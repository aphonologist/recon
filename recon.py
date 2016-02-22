#!/usr/bin/python

import random

def swap_cons(lang):
	index = random.randint(0,len(lang) - 1)
	a = lang[index]
	if index > 0:
		b = lang[index - 1]
		lang[index - 1] = a
		lang[index] = b
	else:
		b = lang[index + 1]
		lang[index + 1] = a
		lang[index] = b
	return lang

def pretty_print(langdict, fn="tree.dot"):
	parents = {}
	for lang in langdict:
		for daughter in langdict[lang]:
			parents[str(daughter)] = str(lang)
	f = open(fn, 'w')
	f.write('digraph family {')
	f.write('\n')
	for x in parents:
		s = '\t' + parents[x] + ' -> ' + x + ';'
		f.write(s)
		f.write('\n')
	f.write('}')
	f.close()

def json_formatter(ranking):
	out = '{\n'
	for i in range(len(ranking) - 1):
		temp = '\t\"' + str(ranking[i]) + '\": [ '
		for j in range(i,len(ranking)):
			if i == j:
				continue
			temp = temp + '\"{}\"'.format(str(j))
			if j < len(ranking) - 1:
				temp = temp + ', '
		temp = temp + ' ]'
		if i < len(ranking) - 2:
			temp = temp + ',\n'
		out = out + temp
	out = out + '\n}'
	return out

def tree2array(tree, langs):
	towrite = ''
	outDict = {}
	for i in range(len(tree)):
		temp = [str(x) for x in langs[i]]
		outDict[i] = temp
	return outDict
	
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

def treeToFile(treeArray, fn="langs.txt"):
	towrite = ""
	for row in treeArray:
		towrite += str(row) + ': ' + ' '.join(str(x) for x in treeArray[row])+'\n'

	f2 = open(fn, 'w')
	f2.write(towrite)
	f2.close()
	return towrite


if __name__ == '__main__':
	import sys
	from language import Language

	# Note for later: this is written for artificial data, we'll have to modify this to read actual data from files

	# Default values
	# Number of constraints -c
	c = 10
	# Maximum number of languages -l
	l = 25
	# Probability that a language will be copied -p
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
	print(randomroot.check_for_loops())
	randomroot.randomize_ranking()
	for c in randomroot.ranking:
		print(c,randomroot.ranking[c])
	print(randomroot.check_for_loops())

	sys.exit()

	(langFam, treeArray) = runMain(args.numCons, args.maxLangs, args.copyProb)

	written = treeToFile(treeArray, fn="langs.txt")

	pretty_print(langFam, fn="tree.dot")
