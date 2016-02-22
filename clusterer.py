import numpy
import fastcluster
import scipy.cluster.hierarchy
from matplotlib.pyplot import show

def parse_file_into_numpy_array(inList):
	proto_distance_array = []
	names = []
	for x in inList:
		linspl = x.split()
		if linspl != []:
			ranking = linspl[1:] # cell [0] is language name
			#print(len(linspl))
			names.append(linspl[0])
			if linspl:
				tonums = [float(x) for x in ranking]
				proto_distance_array.append(tonums)
	#print(proto_distance_array)
	#for pda in proto_distance_array:
	#	print(len(pda))
	#print(len(proto_distance_array))
	return (numpy.array(proto_distance_array), names)

def parse_dict_into_numpy_array(data):
	proto_distance_array = []
	names = []
	for lg in data:
		names.append(lg)
		proto_distance_array.append(data[lg])
	return (numpy.array(proto_distance_array), names)

def build_tree(clustered, names):
	num = len(clustered)
	#nodes = num
	#print(num)
	#print(names)
	out = {}
	mapping = {}
	for i in range(len(clustered)):
		thisNode = "A"+str(num+i+1)
		line = clustered[i]
		#mapping[str(num+i+1)] = thisNode
		if int(line[0]) <= num - 1:
			x = names[int(line[0])]
		else:
			#nodes += 1
			#x = "A"+str(nodes)
			#y = mapping[str(int(line[0]))]
			x = 'A' + str(int(line[0]))
		if int(line[1]) <= num - 1:
			y = names[int(line[1])]
		else:
			#nodes += 1
			#y = "A"+str(nodes)
			#y = mapping[str(int(line[1]))]
			y = 'A' + str(int(line[1]))
		#if 'A' in x or 'A' in y:
		#	if not x in out:
		#		out[x] = []
		#	out[x].append(y)
		#else:
		out[thisNode] = []
		out[thisNode].append(x)
		out[thisNode].append(y)
		#print(x, y, thisNode)
	return out

def getDendogram(data, names=[]):
	temp = fastcluster.linkage(data, method='single')
	#print(temp)
	dendo = build_tree(temp, names)
	#dendo = scipy.cluster.hierarchy.dendrogram(temp, labels=names)
	#newLeaves = []
	#for i in range(len(dendo['leaves'])):
	#	newLeaves.append(names[dendo['leaves'][i]])
	#print(dendo['leaves'])
	#print(newLeaves)
	#show()
	return dendo

def runOld():
	# distances between languages represented in these files:
	#lang_dist_files = ['../experiments/2015-06/pairs_cos.txt', '../experiments/2015-06/pairs_dist.txt', '../experiments/2015-06/pairs_euc.txt', '../experiments/2015-06/pairs_ham.txt']
	lang_dist_files = ['pairs_cos.txt', 'pairs_dist.txt', 'pairs_euc.txt', 'pairs_ham.txt']

	with open(lang_dist_files[1]) as file: # to be replaced once pairwise.py outputs lists
		filecontents = file.readlines()

	(distance_array, names) = parse_file_into_numpy_array(filecontents)
	#print(names)

	print(distance_array)

	#print(fastcluster.linkage(distance_array, method='single'))
	hargle = fastcluster.linkage(distance_array, method='single')

	#threshold=hargle.shape[0]
	#
	#print(hargle)
	#
	#for i in (0, 1):
		#for j in range(threshold):
			##print(hargle[:,i][j])
			#if hargle[:,i][j] < threshold*2:
				#if int(hargle[:,i][j]) < threshold:
					#hargle[:,i][j] = float(names[int(hargle[:,i][j])])
				#else:
					##print(hargle[:,i][j])
					#hargle[:,i][j] = hargle[:,i][j]+100


	#for cellNum in range(hargle.shape[0]):
	#	print(hargle[cellNum])
	#print(fastcluster.single(distance_array))
	#print(it)
	
	#print(hargle)
	
	scipy.cluster.hierarchy.dendrogram(hargle, labels=names)
	
	show()

if __name__ == "__main__":
	runOld()
