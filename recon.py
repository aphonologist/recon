#!/usr/bin/python

import random, copy, sys, numpy, fastcluster, scipy.cluster.hierarchy, matplotlib.pyplot as plt
from language import Language
from family import Family
from get_labeled_nodes import get_nodes
from evaluation import eval

# Note for later: this is written for artificial data, we'll have to modify this to read actual data from files

# Default number of constraints -c
c = 10
# Default maximum number of languages -l
l = 25
# Default probability that a language will be copied -p
p = .1
# Default number of iterations -n
n = 100
# Default evaluation metric -e
e = 'e'
# Default number of families -f
f = 1
# Default cluster method -m
m = 'average'
clustermethod = {'s':'single', 'c':'complete', 'a':'average', 'w':'weighted'}

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
if '-e' in args:
	e = args[args.index('-e') + 1]
if '-f' in args:
	f = int(args[args.index('-f') + 1])
if '-m' in args:
	m = clustermethod[args[args.index('-m') + 1]]
mute = '-mute' in args
noheader = '-noheader' in args

# Help
if '-h' in args:
	print('-c number of constraints; default = 10')
	print('-l maximum number of languages; default = 25')
	print('-p probability that a language will be copied; default = .1')
	print('-n number of iterations of experiment; default = 100')
	print('-e evaluation metric; c = cosine similarity, e = euclidean distance, a = addition')
	print('-f number of families in experiment; default = 1')
	print('-m cluster method; s = single; c = complete; a = average; w = weighted')
	print()
	print('-mute : supress status messages')
	print('-noheader : supress header message')
	sys.exit()

# Generate the constraint set - ints in [1,c]
constraints = [x for x in range(1, c + 1)]

# Flat tree, random tree, test tree
aveprecision = [0.0, 0.0, 0.0]
averecall = [0.0, 0.0, 0.0]
avefscore = [0.0, 0.0, 0.0]

if not noheader:
	# Output header
	print('\t'.join(['c', 'l', 'p', 'n', 'f', 'e', 'm', 'Precision - flat', 'Precision - random', 'Precision - test', 'Recall - flat', 'Recall - random', 'Recall - test', 'F-Score - flat', 'F-Score - random', 'F-Score - test']))

# Run the experiment
for nn in range(n):

	if not mute:
		# Report every n/10 times for boredom reasons
		if nn % 10 == 0:
			print(nn, 'iterations run...')

	# Initialize families
	families = []

	for ff in range(f):
		# Generate random language to use as root for family
		randomroot = Language(constraints, name=str(1000 * ff))
		randomroot.randomize_ranking()
		families.append(Family(randomroot))

	# Evolve family
	for family in families:
		family.evolve(l,p)
	languages = []
	for family in families:
		languages += family.get_leaves()
	languagenames = []
	for language in languages:
		languagenames.append(int(language.__name__))
	languagenames.sort()
	# Output gold tree as a .dot file; then call dot -T png -o [tree].png [tree].dot
#	family.tree_to_dot()

	# Calculate inter-language distances
	lcount = len(languages)
	distances = [[0 for i in range(lcount)] for i in range(lcount)]

	# Evaluation metrics: should be moved into their own .py
	if e == 'c':
		# Cosine Similarity

		# Normalize ranking vectors in languages
		for language in languages:
			language.normalize_ranking()

		# Calculate the distance between languages
		for l1 in range(lcount):
			for l2 in range(l1, lcount):
				# Normalized vectors have length 1, so cosine similarity is just the dot product
				cosine = 0.0
				for i in range(len(languages[l1].normalized_ranking)):
					cosine += languages[l1].normalized_ranking[i] * languages[l2].normalized_ranking[i]
				distances[l1][l2] = cosine
	elif e == 'e':
		# Euclidean Distance
	
		# Get the pairwise comparison vectors
		for language in languages:
			language.get_pairwise()

		# Calculate Euclidean distance between languages
		for l1 in range(lcount):
			for l2 in range(l1,lcount):
				euc = 0.0
				for i in range(len(languages[l1].pairwise_ranking)):
					euc += (languages[l1].pairwise_ranking[i] - languages[l2].pairwise_ranking[i]) ** 2
				distances[l1][l2] = euc ** .5

	elif e == 'a':
		# Simpler distance
	
		# Get the pairwise comparison vectors
		for language in languages:
			language.get_pairwise()

		# Calculate distance between languages
		for l1 in range(lcount):
			for l2 in range(l1,lcount):
				add = 0
				for i in range(len(languages[l1].pairwise_ranking)):
					add += languages[l1].pairwise_ranking[i] - languages[l2].pairwise_ranking[i]
				distances[l1][l2] = add

	# Cluster!
	npdistances = numpy.array(distances)
	thecluster = fastcluster.linkage(npdistances, method=m)
	# Using average as default; options: single, complete, average, weighted

	# Output the cluster as a png
#	dendrogram = scipy.cluster.hierarchy.dendrogram(thecluster, labels=languagenames)
#	plt.savefig('temp.png')
#	plt.cla()

	# Get labeled nodes from gold tree
	goldlabeled = []
	for family in families:
		goldlabeled += get_nodes(family.languages)
	rootall = set(languagenames)
	if rootall not in goldlabeled:
		goldlabeled.append(rootall)

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

	# Generate null hypothesis baseline: flat tree
	flatbaseline = [set(languagenames)]

	# Generate random baseline: random binary tree
	randombaseline = []
	rblstack = [set([str(x) for x in languagenames])]
	while rblstack:
		rbltemp = rblstack.pop()
		randombaseline.append(rbltemp)
		if len(rbltemp) > 1:
			randomsplit = random.randint(1, len(rbltemp) - 1)
			split1 = copy.deepcopy(rbltemp)
			split2 = set([])
			for rbli in range(randomsplit):
				split2.add(split1.pop())
			rblstack.append(split1)
			rblstack.append(split2)
	randombaseline = [x for x in randombaseline if len(x) > 1]

	# In a binary tree, half the nodes are leaf nodes; for evaluation, we may only want internal nodes
#	goldlabeled = [x for x in goldlabeled if len(x) > 1]
#	testlabeled = [x for x in testlabeled if len(x) > 1]
#	flatbaseline = [x for x in flatbaseline if len(x) > 1]
#	randombaseline = [x for x in randombaseline if len(x) > 1]

	# Evaluate
	# Flat tree, random tree, test tree
	flateval = eval(goldlabeled, flatbaseline)
	aveprecision[0] += flateval[0] / n
	averecall[0] += flateval[1] / n
	avefscore[0] += flateval [2] / n

	randomeval = eval(goldlabeled, randombaseline)
	aveprecision[1] += randomeval[0] / n
	averecall[1] += randomeval[1] / n
	avefscore[1] += randomeval [2] / n
	
	testeval = eval(goldlabeled, testlabeled)
	aveprecision[2] += testeval[0] / n
	averecall[2] += testeval[1] / n
	avefscore[2] += testeval [2] / n

# Print results to screen
aveprecision = [round(x,3) for x in aveprecision]
averecall = [round(x,3) for x in averecall]
avefscore = [round(x,3) for x in avefscore]
out = [c, l, p, n, f, e, m] + aveprecision + averecall + avefscore
print('\t'.join([str(x) for x in out]))
