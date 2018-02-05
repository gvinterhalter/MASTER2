import re, sys, os
import mmap
from pprint import pprint
import json

name = 'bla.mgf.windows'
#name = sys.argv[1]

# print(re.sub(" (-?\d.+)", lambda m: ' %f'%10**float(m.group(1)), open(name).read()))

pattern = re.compile(rb"""

BEGIN\ IONS\s+
TITLE=(?P<title>\w+)\s+
PEPMASS=(?P<pepmass>\d+\.\d+)\s+
CHARGE=(?P<charge>\d+)\s+
(?P<values>.+?)
END\ IONS\s+

""", re.X | re.M | re.S)


# text = open(name, 'br').read()
file_id = os.open(name, os.O_RDWR)
mm = mmap.mmap(file_id, 0)

entry_list = []
for m in pattern.finditer(mm):
    entry = m.groupdict()
    entry['charge'] = int(entry['charge'])
    entry['pepmass'] = float(entry['pepmass'])
    entry['title'] = entry['title'].decode('ascii')
    val_iter = map(float, entry['values'].split() ) # ne treba iter(), jer koristim map
    entry['values'] = [(x, 10**y) for x,y in zip(val_iter, val_iter)]
    entry_list.append(entry)
    pprint(entry['title'])

print(json.dumps(entry_list, indent=4))

