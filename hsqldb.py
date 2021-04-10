# pip install JayDeBeApi
import jaydebeapi
from pathlib import Path

__dirpath__ = Path(globals().get("__file__", "./_")).absolute().parent

HSQLDB_JAR_PATH = __dirpath__ / "hsqldb/hsqldb.jar"
DB_PATH = __dirpath__ / "movies-relational/movies"

def pp(cursor, data=None, rowlens=0):
    d = cursor.description
    if not d:
        return "### NO RESULTS ###"
    names = []
    lengths = []
    rules = []
    if not data:
        data = cursor.fetchall(  )
    ptr = 0
    for dd in d:    # iterate over description
        #l = dd[2]
        #if not l:
        #    l = 30             # or default arg ...
        #l = max(l, len(dd[0])) # Handle long names
        l = len(dd[0])
        for r in data:
            l = max(l, len(str(r[ptr])))
        #print(data)
        names.append(dd[0])
        lengths.append(l)
        ptr+=1
    for col in range(len(lengths)):
        if rowlens:
            rls = [len(row[col]) for row in data if row[col]]
            lengths[col] = max([lengths[col]]+rls)
        rules.append("-"*lengths[col])
    format = " ".join(["%%-%ss" % l for l in lengths])
    result = [format % tuple(names)]
    result.append(format % tuple(rules))
    for row in data:
        result.append(format % row)
    return "\n".join(result)


class HSQLDB():
    def __init__(self):
        self.conn = jaydebeapi.connect("org.hsqldb.jdbcDriver",
                                  f"jdbc:hsqldb:file:{DB_PATH};shutdown=true",
                                  {
                                    "urlid": "db1a", 
                                    "username": "SA",
                                    "password": "",
                                    "transiso": "TRANSACTION_READ_COMMITTED",
                                  },
                                  str(HSQLDB_JAR_PATH))
        self.curs = self.conn.cursor()
    
    def query(self, statement):
        self.curs.execute(statement)
        print(pp(self.curs))
        