#!/usr/bin/python2
# coding: utf-8

import xlwt, os, sys, codecs
import unicodecsv as csv

# csv 转 xlsx

def csv_to_execl(csvfiles):
    cnt = 1
    workbook = xlwt.Workbook()

    for csvfile in csvfiles:
        sheet = workbook.add_sheet('Sheet %d' % (cnt))
        cnt += 1
        with open(csvfile, "rb") as f:
            reader = csv.reader(f, delimiter=',')
            for rowi, row in enumerate(reader):
                for coli, value in enumerate(row):
                    sheet.write(rowi, coli, value)

    workbook.save('output.xlsx')

def main():
    csv_to_execl(sys.argv[1:])

if __name__ == "__main__":
    main()
