import re
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateTable

from sqlalchemy.orm import lazyload, joinedload

from sqlalchemy import (
    Table, Column, ARRAY
, Integer, SmallInteger, Float, String, Text, Boolean
, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
, CheckConstraint
)

from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

from sqlalchemy.orm import relationship

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = sa.MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


_all_valid_AA_code = "RKDEQNHSTYCMWAILFVPG"
_invalid_AA_regex = "[^%s]" % _all_valid_AA_code #negacija svih validnih

assert( len(_all_valid_AA_code) == 20 )

def AA_is_valid(seq, invalid_regex=None):
    ''' Return True if no invalid AA code can be found '''
    return not re.search(invalid_regex or _invalid_AA_regex, seq)


sequence_go_assoc = Table("sequence_go_assoc", Base.metadata,
                          Column("sequence_id", String, ForeignKey("sequence.id"), nullable=False),
                          Column("go", Integer, ForeignKey("go_term.go"), nullable=False),
                          PrimaryKeyConstraint("sequence_id", "go"),
                          )

class Protein(Base):
    __tablename__ = "protein"
    id = Column(String, primary_key=True)
    source = Column(String)

    random_sequence_id = Column(String(), ForeignKey("sequence.id"), nullable=True)

    # random_sequence = relationship("Sequence", backref="Protein", uselist=False)


class Sequence(Base):
    __tablename__ = "sequence"

    def __init__(self, *arg, **argv):
        Base.__init__(self, *arg, **argv)
        self.length = len(str(self.sequence))

    id = Column(String, primary_key=True)
    sequence = Column(Text(), nullable=False)
    length = Column(Integer, nullable=False)
    predictable = Column(Boolean)

    protein = relationship(Protein, backref="sequence", uselist=False)

    def calc_is_valide_AA(self):
        return AA_is_valid(self.sequence)

    CheckConstraint(sa.func.char_length(sequence) == length, name="length")

    go_terms = relationship("GOterm", secondary=sequence_go_assoc, backref="sequences")

    def __repr__(self): return f"Sequence<({self.id}, {self.sequence[:20]}...{self.sequence[-3:]}, {self.length})>"


class GOontology(Base):
    __tablename__ = "go_ontology"
    ontology = Column(sa.String(1), primary_key=True)

    def __repr__(self): return f"GOontology<({self.ontology})>"


class GOterm(Base):
    __tablename__ = "go_term"

    go = Column(Integer, primary_key=True, autoincrement=False)
    ontology = Column(sa.String(1), ForeignKey(GOontology.ontology), nullable=False, )

    def __repr__(self): return f"GOterm<(GO:{'%7d'%self.go}, '{self.ontology}')>"


class Predictor(Base):
    __tablename__ = 'predictor'

    name = Column(String, primary_key=True)

    def __repr__(self): return f"Predictor<({self.name})>"


class DisorderPrediction(Base):
    __tablename__ = 'disorder_prediction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sequence_id = Column(String, ForeignKey(Sequence.id), unique=True)
    predictor_name = Column(String, ForeignKey(Predictor.name))

    is_disordered = Column(Boolean, nullable=True)

    sequence = relationship(Sequence, backref="predictionResults")
    predictor = relationship(Predictor, backref="predictionResults")
    raw = relationship("DisorderPredictionRaw", uselist=False)
    regions = relationship("DisorderPredictionRegions")

DP = DisorderPrediction  # short name


class DisorderPredictionRaw(Base):
    __tablename__ = "disorder_prediction_raw"

    pr_id = Column(Integer, ForeignKey(DP.id, ondelete="cascade"), primary_key=True)
    data = Column(ARRAY(Float))

    def __repr__(self):
        short_data = self.data[:20]
        return f"DPRaw<( [{', '.join(['%0.2f'%x for x in short_data])}, ...] )>"

DPRaw = DisorderPredictionRaw  # short name


class DisorderPredictionRegions(Base):
    __tablename__ = "disorder_prediction_regions"


    dp_id = Column(Integer, ForeignKey(DP.id, ondelete="cascade"), nullable=False)
    region = Column(SmallInteger, nullable=False, autoincrement=False)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    PrimaryKeyConstraint(dp_id, region)

    def __repr__(self): return f"DPReg<({self.region}, {self.start}, {self.end})>"


DPReg = DisorderPredictionRegions  # short name

if __name__ == "__main__":
    # for t in Base.metadata.sorted_tables:
    #     print(CreateTable(t))
    #     print("=" * 20)

    pass
