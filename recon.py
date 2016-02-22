#!/usr/bin/python

import random, sys, numpy, fastcluster
from language import Language
from family import Family
from cosine_similarity import cosine

# Note for later: this is written for artificial data, we'll have to modify this to read actual data from files

# Default number of constraints -c
c = 10
# Default maximum number of languages -l
l = 25
# Default probability that a language will be copied -p
p = .001

# Overwrite defaults with values from command line
args = sys.argv[1:]
if '-c' in args:
	c = int(args[args.index('-c') + 1])
if '-l' in args:
	l = int(args[args.index('-l') + 1])
if '-p' in args:
	p = float(args[args.index('-p') + 1])

# Generate the constraint set - ints in [1,c]
constraints = [x for x in range(1, c + 1)]

# Generate random language to use as root for family
randomroot = Language(constraints)
randomroot.randomize_ranking()

# Initialize family
family = Family(randomroot)

# Evolve family
family.evolve(l,p)
languages = family.get_leaves()

# Normalize ranking vectors in languages
for language in languages:
	language.normalize_ranking()

# Calculate the distance between languages
lcount = len(languages)
distances = [[0 for i in range(lcount)] for i in range(lcount)]
for l1 in range(lcount):
	for l2 in range(l1, lcount):
		distances[l1][l2] = cosine(languages[l1], languages[l2])

# Cluster!
npdistances = numpy.array(distances)
