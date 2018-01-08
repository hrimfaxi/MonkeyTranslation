#!/usr/bin/python3
# coding: utf-8

import xlrd, os, sys, codecs
import unicodecsv as csv

# xlsx 转 csv

def csv_from_execl(xlsxfn):
    wb = xlrd.open_workbook(xlsxfn)
    for sh in wb.sheets():
        print(sh.name)
        title = xlsxfn
        for pos in [ title.rfind(".xlsx"), title.rfind(".xls") ]:
            if pos != -1:
                title = title[0:pos]
                break
        else:
            raise RuntimeError("not xlsx or xls")
        ofn = title + u"_" + sh.name + u".csv"
        with open(ofn, "wb") as f:
            wr = csv.writer(f, delimiter=',')

            for rownum in range(sh.nrows):
                v = sh.row_values(rownum)
                if len(v)>0 and isinstance(v[0], (float, )):
                    v[0] = int(v[0])
                if len(v)>1 and isinstance(v[1], (float, )):
                    v[1] = int(v[1])
                wr.writerow(v)
        print (ofn + u" dumped.")

def main():
    csv_from_execl(sys.argv[1])

if __name__ == "__main__":
    main()
