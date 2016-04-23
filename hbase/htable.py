#encoding:UTF-8

import happybase
import hashlib
import os
import sys


reload(sys)
sys.setdefaultencoding('utf8')

class Htable:
    def __init__(self, conn):
        self.conn = happybase.Connection(conn)
    
    def getData(self, tbl, rk_lst, columns):
        self.conn.open()
        if tbl not in self.conn.tables():
            self.conn.close()
            return "TblNotExists"
        self.table = self.conn.table(tbl)
        try:
            res = self.table.rows(rk_lst, columns)
            data = []
            for r in res:
                data.append(r[1])
            self.conn.close()
            return data
        except Exception as e:
            print e
            self.conn.close()
            return None
                
    def putData(self, tbl, rk, inData):
        self.conn.open()
        if tbl not in self.conn.tables():
            self.conn.close()
            return "TblNotExists"
        self.table = self.conn.table(tbl)
        try:
            self.table.put(rk, inData, wal=False)
            self.conn.close()
            return "secc"
        except Exception as e:
            print e
            self.conn.close()
            return None
        
    def delData(self, tbl, rk, cols):
        self.conn.open()
        if tbl not in self.conn.tables():
            self.conn.close()
            return "TblNotExists"
        self.table = self.conn.table(tbl)
        if len(cols) == 0:
            try:
                self.table.delete(rk,wal=False)
                self.conn.close()
                return "secc"
            except Exception:
                self.conn.close()
                return None 
        
        else:
            try:
                self.table.delete(rk, cols, wal=False)
                self.conn.close()
                return "secc"
            except Exception:
                self.conn.close()
                return None   
    
if __name__ == '__main__':
    con_str = 'hbase_host'
    tbl = 'htablename'
    rk_lst = ['rowkey1',
              'rowkey2'
              ]
    ss = unicode("cf:qulifier",'utf-8')
    columns = []
#     columns.append(ss)
    res = Htable(con_str).getData(tbl, rk_lst, columns)
    print ss
    print res
    for r in res:
        print "rk: %s" % (r[0])
        print r[1]
        for q in r[1]:
            print q, r[1][q]
    
    
#     con_str = 'hbase_host'
#     tbl = 'htablename'
#     rk = 'rowkey1'
#               
#     input = {
#         "cf:qulifier1": "1",
#         "cf:qulifier2": "464"
#     }
#     res = Htable(con_str).putData(tbl, rk, input)
#     print res

