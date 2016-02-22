import math

def dominate_relation(lang, conA, conB):
	i = lang.index(str(conA))
	j = lang.index(str(conB))
	if i < j:
		return -1
	return 1

def pair_compare_file(lang):
	name = lang[0][:-1]
	constraints = sorted([int(x) for x in lang[1:]])
	pair_vector = [name]
	for i in range(len(constraints)):
		for j in range(i + 1):
			pair_vector.append(dominate_relation(lang, constraints[i], constraints[j]))
	return pair_vector

def pair_compare(lang):
	constraints = sorted([int(x) for x in lang])
	#print(constraints)
	pair_vector = []
	for i in range(len(constraints)):
		for j in range(i + 1):
			pair_vector.append(dominate_relation(lang, constraints[i], constraints[j]))
	return pair_vector

def difference(pv1, pv2):
	sum = 0
	#print(len(pv1), len(pv2))
	for i in range(len(pv1)):
		#print(i, pv1[i], pv2[i])
		sum += abs(int(pv1[i]) - int(pv2[i]))
	#if sum != 0:
	#	print('WHD',sum)
	return sum

def euclidean_distance(pv1, pv2):
	out = 0
	for i in range(len(pv1)):
		out += (int(pv1[i]) - int(pv2[i])) ** 2
	output = math.sqrt(out)	
	#if output != 0:
	#	print('ED',output)
	return output

def dotproduct(v1, v2):
	return sum(a*b for a,b in zip(v1,v2))

def magnitude(v):
	return math.sqrt(sum(a**2 for a in v))

def cosine_similarity(pv1, pv2):
	output = dotproduct(pv1, pv2)/(magnitude(pv1)*magnitude(pv2))
	#if output != 0:
	#	print('CS',output)
	return output

def hamming(pv1, pv2):
	out = 0
	for i in range(len(pv1)):
		if pv1[i] != pv2[i]:
			out += 1
	#if out != 0:
	#	print('HD',out)
	return out

def spearman(X, Y):
	n = len(X)
	items = sorted([x for x in X])
	rankX = [X.index(i) + 1 for i in items]
	rankY = [Y.index(i) + 1 for i in items]
	d = []
	for i in range(n):
		d.append(rankX[i] - rankY[i])
	d2 = [x**2 for x in d]
	sigma_d2 = 0
	for x in d2:
		sigma_d2 += x
	r = 1 - (6 * sigma_d2) / (n * (n**2 - 1))
	return r

# simple difference
def getSimpleDifference(pair_vectors):
	dists = {}
	for p in pair_vectors:
			pp = pair_vectors[p]
			dists[p] = []
			for v in pair_vectors:
				vv = pair_vectors[v]
				dists[p].append(difference(pp,vv))
	return dists

# euclidean distance
def getEuclideanDistance(pair_vectors):
	dists = {}
	for p in pair_vectors:
		pp = pair_vectors[p]
		dists[p] = []
		for v in pair_vectors:
			vv = pair_vectors[v]
			dists[p].append(euclidean_distance(pp,vv))
	return dists

# cosine similarity
def getCosineSimilarity(pair_vectors):
	dists = {}
	for p in pair_vectors:
		pp = pair_vectors[p]
		dists[p] = []
		for v in pair_vectors:
			vv = pair_vectors[v]
			dists[p].append(cosine_similarity(pp,vv))
	return dists
	
# hamming distance
def getHammingDistance(pair_vectors):
	dists = {}
	for p in pair_vectors:
		pp = pair_vectors[p]
		dists[p] = []
		for v in pair_vectors:
			vv = pair_vectors[v]
			dists[p].append(hamming(pp,vv))
	return dists

# spearman
def getSpearman(langs):
	torts = {}

	for i in langs:
		torts[i] = []
		for j in langs:
			torts[i].append(spearman(langs[i],langs[j]))
	return torts



def getPairwiseVectors(langs):
	pair_vectors = {}
	for l in langs:
		#print(langs[l])
		#print(l)
		pair_vectors[l] = pair_compare(langs[l])
	#p0 = pair_vectors[min(pair_vectors)]

	return pair_vectors

def getPairwiseVectorsFile(langs):
	pair_vectors = []
	for l in langs:
		#print(l)
		pair_vectors.append(pair_compare_file(l))

	#p0 = pair_vectors[0][1:]	#lang 1 minus name

	return pair_vectors

def getFirst(dist):
	firstDist = {}
	for line in dist:
		firstDist[line] = [dist[line][0]]
	return firstDist

def writeDist(dist, fn):
	toWrite = ""
	with open(fn, 'w') as outFile:
		for line in dist:
			toWrite += str(line)+': '+' '.join(str(x) for x in dist[line])+'\n'
		outFile.write(toWrite)

def runOld():
	langs = {}
	with open('langs.txt') as langsFile:
		lines = langsFile.readlines()
	for line in lines:
		(name, protoList) = line.split(':')
		langs[name] = protoList.strip().split(' ')
	
	#(pair_vectors, p0) = getPairwiseVectorsFile(langs)
	#print(pair_vectors)
	pair_vectors = getPairwiseVectors(langs)

	SD = getSimpleDifference(pair_vectors)
	SD_one = getFirst(SD)
	writeDist(SD, "pairs_dist.txt")
	writeDist(SD_one, "dist_from_one_dist.txt")

	ED = getEuclideanDistance(pair_vectors)
	ED_one = getFirst(ED)
	writeDist(ED, "pairs_euc.txt")
	writeDist(ED_one, "dist_from_one_euc.txt")

	CS = getCosineSimilarity(pair_vectors)
	CS_one = getFirst(CS)
	writeDist(CS, "pairs_cos.txt")
	writeDist(CS_one, "dist_from_one_cos.txt")

	HD = getHammingDistance(pair_vectors)
	HD_one = getFirst(HD)
	writeDist(HD, "pairs_ham.txt")
	writeDist(HD_one, "dist_from_one_ham.txt")

	#for p in pair_vectors:
	#	pv = p[1:]
	#	p0 = pair_vectors[0][1:]
	#	#	print(difference(p0, pv), euclidean_distance(p0, pv), cosine_similarity(p0,pv))

if __name__ == "__main__":

	runOld()


