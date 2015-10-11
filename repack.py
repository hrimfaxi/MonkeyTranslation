#!/usr/bin/python
# coding: utf-8

import sys
import os
import ftplib
import glob
import struct
import codecs

if len(sys.argv) < 3:
	print ("Usage: <原文.csv> <翻译.csv>")
	sys.exit(1)

# 原文
fin = codecs.open(sys.argv[1],'r',encoding='utf-8');
# 翻译列表，格式为开始偏移量，结束偏移，原文，翻译
fincsv = codecs.open(sys.argv[2], 'r', encoding='utf-8');
outfile = "out.csv"
# 输出
fout = codecs.open(outfile, 'w', encoding='utf-8');
# 原文的全部内容
csv = fin.read();

fix = 0;
cnt = 0;
# 读入一行
line = fincsv.readline();
# 最后的位置
lastpos = 0;

g_wordlist = [
	[ u'總裁',u'社長' ],
	[ u'萩',u'荻' ],
	[ u'黑',u'黒' ],
	[ u'裡',u'裏' ],
	[ u'關',u'関' ],
	[ u'臟',u'臓' ],
	[ u'幹',u'干' ],
	[ u'滿',u'満' ],
	[ u'待',u'呆' ],
	[ u'參',u'参' ],
	[ u'貓',u'猫' ],
	[ u'晚',u'晩' ],
	[ u'瞭',u'了' ],
	[ u'戀',u'恋' ],
	[ u'來',u'来' ],
	[ u'殘',u'残' ],
	[ u'會',u'会' ],
	[ u'觸',u'触' ],
	[ u'溫',u'温' ],
	[ u'當',u'当' ],
	[ u'隨',u'随' ],
	[ u'穗',u'穂' ],
	[ u'學',u'学' ],
	[ u'獸',u'獣' ],
]

def foreach_replace(string):
	for i in g_wordlist:
		string = string.replace(i[0], i[1])
	return string

compare_csv = foreach_replace(csv)

def get_fuzzy_index_v2(org):
	org = foreach_replace(org)
	fixup_startpos = lastpos
	fixup_startpos = compare_csv.find(org, fixup_startpos)
	if fixup_startpos != -1:
		tlen = len(org)
		print ("%d: 修复: %d, %d %s (lastpos %d)" % (cnt, fixup_startpos, fixup_startpos+tlen, org.encode('utf-8'), lastpos))
		return fixup_startpos, fixup_startpos + tlen

	return -1, -1

while (line):
	# 使用逗号分割
	arr = line.strip().split(',');
	if len(arr) == 4:
		# 开始位置
		pos0 = int(arr[0]);
		# 结束位置
		pos1 = int(arr[1]);
		assert(pos1 > pos0)

		savedpos0 = pos0
		savedpos1 = pos1

		org = arr[2]
		assert(len(org))

		orgfile = csv[pos0:pos1]
		# 翻译中的原文应同原文中的原文相等
		if orgfile != org:
			print ("警告: 翻译中的原文同原文中的原文不相等")
			print ("\t翻译: %s" % (org.encode('utf-8')))
			print ("\t原文: %s" % (orgfile.encode('utf-8')))
			# 采用模糊查找
			pos0, pos1 = get_fuzzy_index_v2(org)
			if pos0 == -1:
			    print ("%d, %d, %s - 未找到，必须人工干预！ lastpos: %d" % (savedpos0, savedpos1, org.encode('utf-8'), lastpos))
			    assert(False)
		# 翻译后的文本
		txt = (arr[3]);
		# 写翻译位置之前的文本
		fout.write(csv[lastpos:pos0] + txt);
		# 不允许发生乱序
		assert(lastpos < pos0)
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
print ("dumped as %s" % (outfile))
