#!/usr/bin/python2
# coding: utf-8

import xlrd, os, sys, codecs
import unicodecsv as csv

# xlsx 转 csv

def csv_from_execl(xlsxfn):
    wb = xlrd.open_workbook(xlsxfn)
    for sh in wb.sheets():
        print(sh.name)
        title = xlsxfn.decode('utf-8')
        title = title[0:title.rfind(".xlsx")]
        ofn = title + u"_" + sh.name + u".csv"
        with open(ofn, "wb") as f:
            wr = csv.writer(f, delimiter=',')

            for rownum in xrange(sh.nrows):
                v = sh.row_values(rownum)
                if isinstance(v[0], (float, )):
                    v[0] = int(v[0])
                    v[1] = int(v[1])
                wr.writerow(v)
        print (ofn + u" dumped.")

def main():
    csv_from_execl(sys.argv[1])

if __name__ == "__main__":
    main()
