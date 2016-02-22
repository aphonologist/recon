def spearman(A, B):
	#nameA = A[0][:-1]
	#nameB = B[0][:-1]
	#X = A[1:]
	#Y = B[1:]
	X = A
	Y = B
	#print(X, Y)
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
	#out = ['{}/{}:'.format(nameA, nameB), r]
	return r
	#print('SRCC',out)
	#return out

def getSpearman(langs):
	torts = {}

	for i in langs:
		torts[i] = []
		for j in langs:
			torts[i].append(spearman(langs[i],langs[j]))
	#		print(temp)


	#		towrite += str(temp[1]) + '\t'
	#f = open('lang_distances.txt', 'w')
	#f.write(towrite)
	#f.close()
	return torts



def runOld():
	langs = {}
	with open('langs.txt') as langsFile:
		lines = langsFile.readlines()
	for line in lines:
		(name, protoList) = line.split(':')
		langs[name] = protoList.strip().split(' ')

	#print(langs)
	SP = getSpearman(langs)
	print(SP)

	towrite = ''
	torout = [x[1] for x in sorted(SP)[::-1]]
	for i in torout:
		towrite += str(i) + '\n'
	g = open('dist_from_one_spear.txt', 'w')
	g.write(towrite)
	g.close()

if __name__ == "__main__":
	runOld()

