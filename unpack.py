#!/usr/bin/python3

import argparse, re, csv

class TransEntry():
	def __init__(self, begin, end, string):
		self.begin = begin
		self.end = end
		self.string = string

def isReservedWord(inp, pos):
	return inp[pos:pos+3] == "<%="

ranges = [
	{"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
	{"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
	{"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
	{"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
	{"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Kana
	{"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
	{"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
	{"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
	{"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
	{"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
	{"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
	{"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}, # included as of Unicode 8.0
	{"from": ord(u"\u3040"), "to": ord(u"\u309f")},		# 平假名
]

# 不包括标点符号
def isCJK(char):
	return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

# 包括标点符号
def isHanzi(ch):
	return ord(ch) >= 0x80

def main():
	transDict = {}
	argparser = argparse.ArgumentParser('unpack')
	argparser.add_argument('input')
	argparser.add_argument('output')
	argparser.add_argument('--unique', '-u', action='store_true')
	args = argparser.parse_args()

	if args.unique:
		print ("Unique mode selected")

	with open(args.input, "r", encoding='utf-8') as fi:
		inp = fi.read()

		curr = begin = end = 0
		caught_hanzi = False
		entries = []
		string = ""

		while curr < len(inp):
			ch = inp[curr]

			if isHanzi(ch):
				string += ch
				if caught_hanzi:
					pass
				else:
					begin = curr
					caught_hanzi = True
			else:
				if caught_hanzi:
					if isReservedWord(inp, curr):
						_ = inp.find("%>", curr) + 2
						string += inp[curr:_]
						curr = _
						continue
					caught_hanzi = False
					end = curr

					if args.unique:
						if string in transDict:
							pass
						else:
							#print (begin, end, string)
							entries.append(TransEntry(begin, end, string))
							transDict[string] = True
					else:
						#print (begin, end, string)
						entries.append(TransEntry(begin, end, string))
					string = ""
			curr += 1

		curr = 0
		for e in entries:
			assert(curr <= e.begin)
			assert(e.begin < e.end)
			assert(inp[e.begin:e.end] == e.string)
			curr = e.end
			# print (e.begin, e.end, e.string)

	cjk = 0
	with open(args.output, "w", encoding='utf-8') as fo:
		csv_writer = csv.writer(fo)
		for e in entries:
			csv_writer.writerow([e.begin, e.end, e.string])
			for ch in e.string:
				if isCJK(ch):
					cjk += 1
	print ("{}: {} entries exported. {} CJK charactors found.".format(args.output, len(entries), cjk))

if __name__ == "__main__":
	main()
