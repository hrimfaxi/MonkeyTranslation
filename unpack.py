#!/usr/bin/python
import sys
import os
import ftplib
import glob
import struct
import codecs



fin = codecs.open('1.txt','r',encoding='utf-8');
fout = codecs.open('out.csv', 'w', encoding='utf-8');
origcsv = fin.read();
lastWide = False;
wdstr = u'';
wdstart = 0;
wdend = 0;

i = 0;

reservedStr = '<%=name%>';

while(i < len(origcsv)):
	ch = origcsv[i];
	isWide = ord(ch) > 127;
	if (isWide) :
		if (not lastWide) :
			wdstr = ch;
			wdstart = i;
		else :
			wdstr += ch;
	else: 
		if (lastWide) :
			if (origcsv[i:i + len(reservedStr)] == reservedStr) :
				i += len(reservedStr);
				wdstr += reservedStr;
				continue;
				
			wdend = i;
			r = u'';
			r += str(wdstart) + ',' + str(wdend) + ',';
			r += wdstr;
			r += '\r\n';
			fout.write(r);
	lastWide = isWide;
	i += 1;
