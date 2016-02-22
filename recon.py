#!/usr/bin/python

import random
import sys
from language import Language
from family import Family

def runMain(numCons, maxLangs, copyProb):
	protoLang = [str(i) for i in range(numCons)]
	#print(protoLang)

	langs = {'0': protoLang}

	langFam = {}

	langFam[str(len(langs) - 1)] = []

	def count_leaves(langdict):
		out = 0
		for lang in langdict:
			if not langdict[lang]:
				out += 1
		return out

	c = count_leaves(langFam)

	while c < maxLangs:
		for i in range(len(langs)):
			p = random.random()
			if p > copyProb: # ranking changes
				#print(langFam, langs)
				if not langFam[str(i)]:
					langs[str(i)] = swap_cons(langs[str(i)])[:]
			else: # copy language
				for num in range(2):
					langFam[str(len(langs))] = []
					langFam[str(i)].append(len(langs))
					langs[str(len(langs))] = langs[str(i)]
		c = count_leaves(langFam)
	
	leafs = {}
	for lang in langFam:
		if not langFam[lang]:
			leafs[lang] = langs[lang]

	return(langFam, leafs)

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
languagefamily = Family(randomroot)

# Evolve family
languagefamily.evolve(l,p)
