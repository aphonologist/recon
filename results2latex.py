#!/usr/bin/env python3

import csv
import argparse
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.mlab as mlab
from matplotlib import cm
import numpy as np

def getData(fn):
	# initialise dataArray
	global FRT
	global nums
	dataArray = {}
	nums = [ 2, 4, 8, 16, 32, 64, 128 ]
	probs = [ 0.1, 0.01, 0.001 ]
	FRT = ['flat', 'random', 'test']
	for prob in probs:
		#print(prob)
		dataArray[prob] = {}
		for numi in nums:
			dataArray[prob][numi] = {}
			for numj in nums:
				dataArray[prob][numi][numj] = {}
				for FRTtype in FRT:
					dataArray[prob][numi][numj][FRTtype] = {'precision': 9.999, 'recall': 9.999}

	for prob in probs:
		pass
	#	dataArray[prob] = {}
	#	for numi in nums:
	#		dataArray[prob][numi] = {}
	#		for numj in nums:
	#			dataArray[prob][numi][numj] = {}
	#			for FRTtype in FRT:
	#				dataArray[prob][numi][numj][FRTtype] = {'precision': None, 'recall': None}

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
					#print(row)
					#print(PRF, FRTtype, row[PRF[FRTtype][0]])
					#print(p, c, l, FRTtype, dataArray[p][c][l])
					dataArray[p][c][l][FRTtype]['precision'] = row[PRF[FRTtype][0]]
					dataArray[p][c][l][FRTtype]['recall'] = row[PRF[FRTtype][1]]
	return dataArray

def printTable(subArray, prec):
	global FRT
	global nums
	header = """\\begin{tabular}{cc|cc|cc|cc|cc|cc|cc|cc}
    ~ & ~ & \\multicolumn{14}{c}{\\# languages} \\\\
    ~ & ~ & \\multicolumn{2}{c}{2} & \\multicolumn{2}{c}{4} & \\multicolumn{2}{c}{8} & \\multicolumn{2}{c}{16} & \\multicolumn{2}{c}{32} & \\multicolumn{2}{c}{64} & \\multicolumn{2}{c}{128} \\\\
    \\multicolumn{2}{c|}{\\# cons} & P & R & P & R & P & R & P & R & P & R & P & R & P & R \\\\"""

	footer = """\\hline
	\\end{{tabular}}
	\\caption{{Precision and recall of $BF$, $BR$, and $T'$ with $p={}$}}\\label{{{}results}}
	\\end{{table*}}""".format(prec, str(prec).lstrip('0'))


	outrows = []
	for cons in nums:
		superRow = """\\hline
     \\multirow{{3}}{{*}}{{{}}} & """.format(cons)

		rows = []
		passed = False
		for (shorter, longer) in zip(['BF', 'BR', 'T\''], FRT):
			thisRow = "${}$ & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f} \\\\ ".format(shorter, #
				float(subArray[cons][2][longer]['precision']),
				float(subArray[cons][2][longer]['recall']),
				float(subArray[cons][4][longer]['precision']),
				float(subArray[cons][4][longer]['recall']),
				float(subArray[cons][8][longer]['precision']),
				float(subArray[cons][8][longer]['recall']),
				float(subArray[cons][16][longer]['precision']),
				float(subArray[cons][16][longer]['recall']),
				float(subArray[cons][32][longer]['precision']),
				float(subArray[cons][32][longer]['recall']),
				float(subArray[cons][64][longer]['precision']),
				float(subArray[cons][64][longer]['recall']),
				float(subArray[cons][128][longer]['precision']),
				float(subArray[cons][128][longer]['recall'])
			)
			if passed:
				thisRow = "~ & "+thisRow
			rows.append(thisRow)
			passed = True
		outrows.append(superRow+'\n'.join(rows))
#     $BF$ & 1.000 & 0.500 & 1.000 & 0.245 & 1.000 & 0.122 & 1.000 & 0.061 & 1.000 & 0.030 & 1.000 & & 1.000 &\\
# ~ & $BR$ & 1.000 & 0.500 & 0.566 & 0.387 & 0.212 & 0.171 & 0.098 & 0.085 & 0.043 & 0.039 & & & & \\
# ~ & $T'$ & 1.000 & 0.500 & 0.603 & 0.417 & 0.331 & 0.276 & 0.197 & 0.178 & 0.135 & 0.127 & & & & \\"""

	return header+'\n'.join(outrows)+footer



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='process results into latex table')
	parser.add_argument('dataFile', help='data file input')
	parser.add_argument('-g', '--graph', help='make graph', default=False, action="store_true")

	args = parser.parse_args()

	dataArray = getData(args.dataFile)
	#print(dataArray)

	if not args.graph:
		tableOut1 = printTable(dataArray[0.1], 0.1)
		print(tableOut1, '\n')
		tableOut2 = printTable(dataArray[0.01], 0.01)
		print(tableOut2, '\n')
		tableOut3 = printTable(dataArray[0.001], 0.001)
		print(tableOut3, '\n')
	else:


		def getMatrixFromData(FRType, PR):
			outMatrix = {}
			for prob in dataArray:
				#outMatrix[prob] = {}
				outMatrix[prob] = []
				for consts in nums: #dataArray[prob]:
					toAppend = []
					for langs in nums: #dataArray[prob][consts]:
						#outMatrix[prob][consts].append(dataArray[prob][consts][langs][FRType][PR])
						thisValue = float(dataArray[prob][consts][langs][FRType][PR])
						if thisValue > 1.000:
							toAppend.append(np.nan)
						else:
							toAppend.append(thisValue)

					outMatrix[prob].append(toAppend)
						#print(langs, dataArray[prob][consts][langs][FRType][PR])
			return outMatrix
#					print(consts)
#					dataArray[p][c][l][FRTtype]['recall']

		testMatrixPrec = getMatrixFromData('test', 'recall')
		flatMatrixPrec = getMatrixFromData('flat', 'recall')
		randMatrixPrec = getMatrixFromData('random', 'recall')

		testMatrixRecall = getMatrixFromData('test', 'precision')
		flatMatrixRecall = getMatrixFromData('flat', 'precision')
		randMatrixRecall = getMatrixFromData('random', 'precision')

		testMatrixFscore = {}
		flatMatrixFscore = {}
		randMatrixFscore = {}
		for thisP in [0.1, 0.01, 0.001]:
			thisTestMatrixPrec = np.array(testMatrixPrec[thisP])
			thisTestMatrixRecall = np.array(testMatrixRecall[thisP])
			testMatrixFscore[thisP] = 2 * thisTestMatrixPrec * thisTestMatrixRecall / (thisTestMatrixPrec+thisTestMatrixRecall)

			thisFlatMatrixPrec = np.array(flatMatrixPrec[thisP])
			thisFlatMatrixRecall = np.array(testMatrixRecall[thisP])
			flatMatrixFscore[thisP] = 2 * thisFlatMatrixPrec * thisFlatMatrixRecall / (thisFlatMatrixPrec+thisFlatMatrixRecall)

			thisRandMatrixPrec = np.array(randMatrixPrec[thisP])
			thisRandMatrixRecall = np.array(testMatrixRecall[thisP])
			randMatrixFscore[thisP] = 2 * thisRandMatrixPrec * thisRandMatrixRecall / (thisRandMatrixPrec+thisRandMatrixRecall)


		#print(testMatrixFscore)
		#testMatrixFscore = 2*testMatrixPrec*testMatrixRecall/(testMatrixPrec+testMatrixRecall)
		#flatMatrixFscore = 2*flatMatrixPrec*flatMatrixRecall/(flatMatrixPrec+flatMatrixRecall)
		#randMatrixFscore = 2*randMatrixPrec*randMatrixRecall/(randMatrixPrec+randMatrixRecall)

		#print(testMatrixPrec)
		#flatMatrix = {}
		#randMatrix = {}


		DATA = {}
		DATA['p'] = {'test': testMatrixPrec, 'flat': flatMatrixPrec, 'rand': randMatrixPrec}
		DATA['r'] = {'test': testMatrixRecall, 'flat': flatMatrixRecall, 'rand': randMatrixRecall}
		DATA['f'] = {'test': testMatrixFscore, 'flat': flatMatrixFscore, 'rand': randMatrixFscore}
		#print(DATA['f']['test'][0.1])
		#print(DATA['f']['rand'][0.1])
		#hargle = bargle

		actualLabels = [2, 4, 8, 16, 32, 64, 128]

		for thisP in [0.1, 0.01, 0.001]:

			for thisType in ['p', 'r', 'f']:  # precision, recall, fscore

				#delta = 0.1
				#x = np.arange(0, 128, delta)
				#y = np.arange(0, 128, delta)
				x = [1, 2, 3, 4, 5, 6, 7] # nums
				y = [1, 2, 3, 4, 5, 6, 7] # nums
				X, Y = np.meshgrid(x, y)
				#print(testMatrixPrec[0.1])
				#print(X, Y)

				fig = plt.figure()
				#ax = fig.gca(projection='3d')
				fig.patch.set_facecolor('white')
				fig.patch.set_alpha(0.2)
				ax = fig.add_subplot(111,projection='3d')
				ax.patch.set_facecolor('white')
				ax.patch.set_alpha(0)

				#ax.xaxis.set_scale('log')
				#ax.yaxis.set_scale('log')

				fig.gca().set_yticklabels(actualLabels)
				fig.gca().set_xticklabels(actualLabels)
				fig.gca().set_ylabel("constraints")
				fig.gca().set_xlabel("languages")
				fig.gca().set_zlabel("fscore")


				ax.w_xaxis._axinfo.update({'grid' : {'color': (0.7, 0.7, 0.7, 1)}})
				ax.w_yaxis._axinfo.update({'grid' : {'color': (0.7, 0.7, 0.7, 1)}})
				ax.w_zaxis._axinfo.update({'grid' : {'color': (0.7, 0.7, 0.7, 1)}})

				surfs = []
				for (matrix, cl, lb) in zip(
					(DATA[thisType]['test'], DATA[thisType]['flat'], DATA[thisType]['rand']),
					#(testMatrixPrec, flatMatrixPrec, randMatrixPrec),
					('r', 'c', 'y'),
					('T\'', 'BF', 'BR')
					):
					Z = np.array(matrix[thisP])
					print(thisType, thisP, Z)

					#fig = plt.figure()
					#fig.figsize = fig_size
					#ax = fig.add_subplot(projection='3d')

		#			ax.plot_wireframe(X, Y, Z,
		#	                 rstride = 1,
		#	                 cstride = 1)
					#surf = ax.plot_surface(X, Y, Z,
					thisGraph = ax.plot_wireframe(X, Y, Z,
						rstride = 1,
						cstride = 1,
						#cmap=cm.RdPu,
						antialiased = True,
						color = cl,
						label = lb)
					surfs.append(thisGraph)
		#		cset = ax.contourf(X, Y, Z,
		#                   zdir = 'x',
		#                   offset = -3)
		#
		#		cset = ax.contourf(X, Y, Z,
		#                   zdir = 'y',
		#                   offset = 2)
		#
		#		cset = ax.contourf(X, Y, Z,
		#                   zdir = 'z',
		#                   offset = -1.5)



				#ax.view_init(elev=30, azim=-36)
				#ax.dist=12
				#fig.colorbar(surf, shrink=0.5, aspect=5)
				ax.legend()
				#plt.show()
				for thisFormat in ["pdf", "svg", "png"]:
					extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
					#fig.savefig('ax2_figure.png', bbox_inches=extent)
					#plt.savefig('{}{}.{}'.format(thisType, str(thisP).replace('.', ''), thisFormat), format=thisFormat)
					plt.savefig('{}{}.{}'.format(thisType, str(thisP).replace('.', ''), thisFormat), format=thisFormat, bbox_inches=extent.expanded(1.05, 1.05))

				#surf = ax.plot_surface(X, Y, Exp_Fric_map, alpha = 1, rstride=1, cstride=1, cmap=cm.winter, linewidth=0.5, antialiased=True)
