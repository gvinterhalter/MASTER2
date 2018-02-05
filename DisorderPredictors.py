import os, subprocess, tempfile
import re
from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from concurrent.futures import ThreadPoolExecutor
from numba import njit

from tqdm import tqdm

tConvertResult = List[Tuple[bool, float]]
tRegionList = List[Tuple[int, int]]
tPredictionResult = Tuple[str, tConvertResult, tRegionList]


class DissPredictor(metaclass=ABCMeta):
    default_basedir = 'Predictors'
    _read_from_file_ = None  # To be overridden
    name = None

    def __init__(self, basedir: str = None):
        self.basedir = basedir

    def _get_path_(self, name: str) -> str:
        basedir = self.basedir or self.default_basedir
        return os.path.join(basedir, name)

    @abstractmethod
    def get_cmd(self, filename: str = None, sequence: str = None) -> List[str]:
        pass

    @abstractmethod
    def convert(self, prediction_output: str) -> tConvertResult:
        pass

    def run(self, seq: Tuple[str, str]) -> tPredictionResult:
        id, sequence = seq
        if self._read_from_file_:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
                file.write(sequence)
                filename = file.name
                file.close()  # stupid windows
                cmd = self.get_cmd(filename=filename)
                r = subprocess.run(cmd, stdout=subprocess.PIPE)
                os.remove(file.name)  # stupid windows #TODO ovo treba u catch block
        else:
            cmd = self.get_cmd(sequence=sequence)
            r = subprocess.run(cmd, stdout=subprocess.PIPE)

        if r.returncode != 0:  # error
            # ko god da je prog. ovaj prediktor, pa valjda stderr umesto stdout
            # msg = " ".join(cmd) + "\n" + r.stdout.decode("ascii")
            # raise RuntimeError(msg)
            return id, None, None

        output = r.stdout.decode("ascii")
        result = self.convert(output)
        regions = DissPredictor.get_regions(result)

        return id, result, regions

    @staticmethod
    @njit
    def get_regions(output: List) -> tRegionList:
        regions = []
        current = False
        for i, (d, p) in enumerate(output):
            if current != d:
                current = d
                if current is True:
                    regions.append((i, len(output)))  # da ne bi ostalo (start, None) za poslednji
                else:
                    start, _ = regions.pop()
                    regions.append((start, i))  # start, end, (length = end - start)
        return regions


class VSL2b(DissPredictor):
    name = "VSL2b"
    _read_from_file_ = True
    _pattern_ = re.compile(r"^\d+\s+[A-Z]+\s+([01]\.\d+)\s+([.D])", re.MULTILINE)

    def get_cmd(self, filename: str = None, sequence: str = None) -> List[str]:
        return ["java", "-jar", self._get_path_("VSL2.jar"), "-s:" + filename]

    def convert(self, prediction_output: str) -> tConvertResult:
        match_result = re.findall(VSL2b._pattern_, prediction_output)
        return [(d == 'D', float(num)) for num, d in match_result]


# vsl2b = VSL2b()
#
# from models import *
#
# engine = sa.create_engine("postgresql://goksi:124@localhost/master", echo=False)
# Session = sa.orm.sessionmaker(bind=engine)
#
# session = Session()
# seq_list = session.query(Sequence.id, Sequence.sequence).all()
# session.close()
#
#
# def predict(seq_list, predictor: Predictor):
#     n = len(seq_list)
#     with ThreadPoolExecutor(max_workers=2) as executor:
#         for id, res, reg in tqdm(executor.map(predictor.run, seq_list, chunksize=n // 4), total=n):
#             if res is None:
#                 continue  # predikcija nije uspela, nedozvoljena slova ili ...
#
#             session = Session()
#             dp = DisorderPrediction(sequence_id=id, predictor_name=predictor.name)
#             dp.raw = DPRaw(data=[x for (_, x) in res])
#             dp.regions = [DPReg(region=i, start=s, end=e) for i, (s, e) in enumerate(reg)]
#             dp.is_disordered = any(e - s >= 40 for s, e in reg)
#             session.add(dp)
#             session.commit()
#
#             pass
#
#
# predict(seq_list, vsl2b)
