#!/usr/bin/python
import sys
import os
import ftplib
import glob
import struct
import codecs



fin = codecs.open('1.txt','r',encoding='utf-8');
fincsv = codecs.open('all.csv', 'r', encoding='utf-8');
fout = codecs.open('final.csv', 'w', encoding='utf-8');
csv = fin.read();


fix = 0;
cnt = 0;
line = fincsv.readline();
lastpos = 0;


while (line):
	arr = line.strip().split(',');
	if ((len(arr) == 3) or ((len(arr) == 4) and (arr[4] == ''))):
		pos0 = int(arr[0]);
		pos1 = int(arr[1]);
		txt = (arr[2]);
		fout.write( csv[lastpos:pos0] + txt);
		lastpos = pos1;
	else:
		print('error at: ' );
		print(line);

		
	cnt += 1;
	if (cnt % 10000 == 0):
		print(cnt);

		
	line = fincsv.readline();

fout.write(csv[lastpos:]);