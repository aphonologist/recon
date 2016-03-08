#!/usr/bin/env python3

import csv
import argparse

def getData(fn):
	# initialise dataArray
	global FRT
	global nums
	dataArray = {}
	nums = [ 2, 4, 8, 16, 32, 64, 128 ]
	probs = [ 0.1, 0.01, 0.001 ]
	FRT = ['flat', 'random', 'test']
	for prob in probs:
		dataArray[prob] = {}
		for numi in nums:
			dataArray[prob][numi] = {}
			for numj in nums:
				dataArray[prob][numi][numj] = {}
				for FRTtype in FRT:
					dataArray[prob][numi][numj][FRTtype] = {'precision': None, 'recall': None}

		# file columns:
		# 0 c
		# 1 l
		# 2 p
		# 3 n
		# 4 f
		# 5 e
		# 6 m
		# 7 Precision - flat
		# 8 Precision - random
		# 9 Precision - test
		# 10 Recall - flat
		# 11 Recall - random
		# 12 Recall - test
		# 13 F-Score - flat
		# 14 F-Score - random
		# 15 F-Score - test
		PRF = {'flat': [7, 10, 13], 'random': [8, 11, 14], 'test': [9, 12, 15]}

		# load file
		with open(fn, 'r') as tsvFile:
			data = csv.reader(tsvFile, delimiter='\t')

			for row in data:
				#print(row)

				for FRTtype in FRT:
					p = float(row[2])
					c = int(row[0])
					l = int(row[1])
					dataArray[p][c][l][FRTtype]['precision'] = row[PRF[FRTtype][0]]
					dataArray[p][c][l][FRTtype]['recall'] = row[PRF[FRTtype][1]]
	return dataArray

def printTable(subArray, prec):
	global FRT
	global nums
	header = """\\begin{{tabular}}{{cc|cc|cc|cc|cc|cc|cc|cc}}
    ~ & ~ & \\multicolumn{{7}}{{c}}{{\\# languages}} \\\\
    ~ & ~ & \\multicolumn{{2}}{{c}}{{2}} & \\multicolumn{{2}}{{c}}{{4}} & \\multicolumn{{2}}{{c}}{{8}} & \\multicolumn{{2}}{{c}}{{16}} & \\multicolumn{{2}}{{c}}{{32}} & \\multicolumn{{2}}{{c}}{{64}} & \\multicolumn{{2}}{{c}}{{128}} \\\\
    \\multicolumn{{2}}{{c|}}{{\\# cons}} & P & R & P & R & P & R & P & R & P & R & P & R & P & R \\\\"""

	footer = """\\hline
	\\end{{tabular}}
	\\caption{{Precision and recall of $BF$, $BR$, and $T'$ with $p={}$}}\\label{{{}results}}
	\\end{{table*}}""".format(prec, str(prec).lstrip('0'))


	outrows = []
	for cons in nums:
		superRow = """\\hline
     \\multirow{{3}}{{*}}{{{}}} & """.format(cons)

		rows = []
		for (shorter, longer) in zip(['BF', 'BR', 'T\''], FRT):
			thisRow = "${}$ & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} \\ ".format(shorter, #
				subArray[cons][2][longer]['precision'],
				subArray[cons][2][longer]['recall'],
				subArray[cons][4][longer]['precision'],
				subArray[cons][4][longer]['recall'],
				subArray[cons][8][longer]['precision'],
				subArray[cons][8][longer]['recall'],
				subArray[cons][16][longer]['precision'],
				subArray[cons][16][longer]['recall'],
				subArray[cons][32][longer]['precision'],
				subArray[cons][32][longer]['recall'],
				subArray[cons][64][longer]['precision'],
				subArray[cons][64][longer]['recall'],
				subArray[cons][128][longer]['precision'],
				subArray[cons][128][longer]['recall']
			)
			rows.append(thisRow)
		outrows.append(superRow+'\n'.join(rows))
#     $BF$ & 1.000 & 0.500 & 1.000 & 0.245 & 1.000 & 0.122 & 1.000 & 0.061 & 1.000 & 0.030 & 1.000 & & 1.000 &\\
# ~ & $BR$ & 1.000 & 0.500 & 0.566 & 0.387 & 0.212 & 0.171 & 0.098 & 0.085 & 0.043 & 0.039 & & & & \\
# ~ & $T'$ & 1.000 & 0.500 & 0.603 & 0.417 & 0.331 & 0.276 & 0.197 & 0.178 & 0.135 & 0.127 & & & & \\"""

	return header+'\n'.join(outrows)+footer



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='process results into latex table')
	parser.add_argument('dataFile', help='data file input')

	args = parser.parse_args()

	dataArray = getData(args.dataFile)
	#print(dataArray)
	tableOut1 = printTable(dataArray[0.1], 0.1)
	print(tableOut1, '\n')
	tableOut2 = printTable(dataArray[0.01], 0.01)
	print(tableOut2, '\n')
	tableOut3 = printTable(dataArray[0.001], 0.001)
	print(tableOut3, '\n')
