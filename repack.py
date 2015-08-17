#!/usr/bin/python
# coding: utf-8

import sys
import os
import ftplib
import glob
import struct
import codecs

# 原文
fin = codecs.open('1.txt','r',encoding='utf-8');
# 翻译列表，格式为开始偏移量，结束偏移，原文，翻译
fincsv = codecs.open('all.csv', 'r', encoding='utf-8');
# 输出
fout = codecs.open('final.csv', 'w', encoding='utf-8');
# 原文的全部内容
csv = fin.read();

fix = 0;
cnt = 0;
# 读入一行
line = fincsv.readline();
# 最后的位置
lastpos = 0;

while (line):
	# 使用逗号分割
	arr = line.strip().split(',');
	if len(arr) == 4:
		# 开始位置
		pos0 = int(arr[0]);
		# 结束位置
		pos1 = int(arr[1]);
		# 翻译后的文本
		txt = (arr[3]);
		# 写翻译位置之前的文本
		fout.write(csv[lastpos:pos0] + txt);
		# 更新最后位置
		lastpos = pos1;
	else:
		# 报错
		print('error at: ' );
		print(line)
		assert(False)
		
	# 记数+1
	cnt += 1;
	# 每10000个更新打印
	if (cnt % 10000 == 0):
		print(cnt);
		
	# 读下一行
	line = fincsv.readline();

# 写最后的
fout.write(csv[lastpos:]);
print ("%d line imported" % (cnt))
