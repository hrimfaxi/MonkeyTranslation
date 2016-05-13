#!/usr/bin/python
# coding: utf-8

import sys
import os
import ftplib
import glob
import struct
import codecs

# 导出脚本

if len(sys.argv) < 3:
    print ("Usage: %s <原文.csv> <输出文件.csv>" % (sys.argv[0]))
    sys.exit(1)

# 原文/CSV格式
fin = codecs.open(sys.argv[1],'r',encoding='utf-8');
# 输出CSV文件 (转化为人类可读形式)
fout = codecs.open(sys.argv[2], 'w', encoding='utf-8');
# 得到整个原文
origcsv = fin.read();
lastWide = False;
wdstr = u'';
wdstart = 0;
wdend = 0;

i = 0;

# 保留的字符串列表
reservedStrList = [
	'<%=name%>',
#	'{CR}',
#	'{LF}',
]

while(i < len(origcsv)):
	ch = origcsv[i];
	# 是汉字？
	isWide = ord(ch) > 127;
	if (isWide) :
		# 上一个不是汉字
		if (not lastWide) :
			# 记录字符串
			wdstr = ch;
			# 记录下偏移量
			wdstart = i;
		else :
			wdstr += ch;
	else:
		# 不是汉字
		# 上一个是汉字？
		if (lastWide) :
			# 是保留字？
			foundReservedStr = False
			for reservedStr in reservedStrList:
				if origcsv[i:i + len(reservedStr)] == reservedStr:
					# 加入保留字长度到偏移量
					i += len(reservedStr);
					# 加入保留字到wdstr
					wdstr += reservedStr;
					# 继续
					foundReservedStr = True
					break

			if foundReservedStr:
				continue

			# 记录结束字
			wdend = i;
			# 输出格式: 开始偏移，结束偏移，字符串
			r = u'';
			r += str(wdstart) + ',' + str(wdend) + ',';
			r += wdstr;
			r += '\r\n';
			# 输出
			fout.write(r);
	# 记录上一个字符是否为汉字
	lastWide = isWide;
	# 下一个字符
	i += 1;
