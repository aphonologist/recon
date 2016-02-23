#!/usr/bin/python

import random, sys, numpy, fastcluster, scipy.cluster.hierarchy, matplotlib.pyplot as plt
from language import Language
from family import Family
from get_labeled_nodes import get_nodes

# Note for later: this is written for artificial data, we'll have to modify this to read actual data from files

# Default number of constraints -c
c = 10
# Default maximum number of languages -l
l = 25
# Default probability that a language will be copied -p
p = .001
# Default number of iterations -n
n = 100

# Overwrite defaults with values from command line
args = sys.argv[1:]
if '-c' in args:
	c = int(args[args.index('-c') + 1])
if '-l' in args:
	l = int(args[args.index('-l') + 1])
if '-p' in args:
	p = float(args[args.index('-p') + 1])
if '-n' in args:
	n = int(args[args.index('-n') + 1])
# Help
if '-h' in args:
	print('-c number of constraints; default = 10')
	print('-l maximum number of languages; default = 25')
	print('-p probability that a language will be copied; default = .001')
	print('-n number of iterations of experiment; default = 100')
	sys.exit()

# Generate the constraint set - ints in [1,c]
constraints = [x for x in range(1, c + 1)]

aveprecision = 0.0
averecall = 0.0
avefscore = 0.0

for nn in range(n):

	# Report every n/10 times for boredom reasons
	if nn % 10 == 0:
		print(nn, 'iterations run...')

	# Generate random language to use as root for family
	randomroot = Language(constraints)
	randomroot.randomize_ranking()

	# Initialize family
	family = Family(randomroot)

	# Evolve family
	family.evolve(l,p)
	languages = []
	languages = family.get_leaves()
	languagenames = []
	for language in languages:
		languagenames.append(int(language.__name__))
	languagenames.sort()

	# Normalize ranking vectors in languages
	for language in languages:
		language.normalize_ranking()

	# Calculate the distance between languages
	lcount = len(languages)
	distances = [[0 for i in range(lcount)] for i in range(lcount)]
	for l1 in range(lcount):
		for l2 in range(l1, lcount):
			# Normalized vectors have length 1, so cosine similarity is just the dot product
			cosine = 0.0
			for i in range(len(languages[l1].normalized_ranking)):
				cosine += languages[l1].normalized_ranking[i] * languages[l2].normalized_ranking[i]
			distances[l1][l2] = cosine

	# Cluster!
	npdistances = numpy.array(distances)
	thecluster = fastcluster.linkage(npdistances, method='single')
	# Output the cluster as a png
	# dendrogram = scipy.cluster.hierarchy.dendrogram(thecluster, labels=languagenames)
	# plt.savefig('temp.png')
	# plt.cla()

	# Get labeled nodes from gold tree
	goldlabeled = get_nodes(family.languages)

	# Parse cluster results into a tree
	num = len(thecluster)
	testfamily = {}
	mapping = {}
	for i in range(len(thecluster)):
		thisNode = 'A' + str(num + i + 1)
		line = thecluster[i]
		if int(line[0]) <= num:
			x = int(languagenames[int(line[0])])
		else:
			x = 'A' + str(int(line[0]))
		if int(line[1]) <= num:
			y = int(languagenames[int(line[1])])
		else:
			y = 'A' + str(int(line[1]))
		testfamily[thisNode] = [x,y]
		if x not in testfamily:
			testfamily[x] = []
		if y not in testfamily:
			testfamily[y] = []

	# Get labeled nodes from test tree
	testlabeled = get_nodes(testfamily)

	##to add: flat tree baseline, random binary tree baseline

	# Evaluate
	numbersharednodes = 0.0
	for node in goldlabeled:
		if node in testlabeled:
			numbersharednodes += 1
	precision = numbersharednodes / len(testlabeled)
	recall = numbersharednodes / len(goldlabeled)
	fscore = 2 * precision * recall / (precision + recall)

	aveprecision += precision / n
	averecall += recall / n
	avefscore += fscore / n

print(aveprecision, averecall, avefscore)
