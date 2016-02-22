#!/usr/bin/env python3

def invertdict(treedict):
	output = {}
	for parent in treedict:
		for daughter in treedict[parent]:
			output[daughter] = parent
	for parent in treedict:
		if parent not in output:
			output[parent] = -1
	return output

def pathtoroot(treedict,a):
	path = str(a)
	x = a
	while treedict[x] > -1:
		path += '-' + str(treedict[x])
		x = treedict[x]
	else:
		return path

def nodedist(treedict,x,y):
	xroot = pathtoroot(treedict,x).split('-')
	yroot = pathtoroot(treedict,y).split('-')
	lca = ''
	for node in xroot[::-1]:
		if node in yroot:
			lca = node
	return xroot.index(lca) + yroot.index(lca)

def allnodedists(treedict):
	output = []
	srtdnodes = sorted([node for node in treedict])
	for a in srtdnodes:
		for b in srtdnodes:
			output.append(nodedist(treedict,a,b))
	return output


def runOld():
	# daughter:parent
	"""  
	      1
	     / \
	    2   3
	       /|\
	      4 5 6
	     /   / \
	    7   8   9 
	"""
	extree = {
	1:-1,
	2:1,
	3:1,
	4:3,
	5:3,
	6:3,
	7:4,
	8:6,
	9:6
	}

	print(extree)

	ptodex = {
	1:[2,3],
	2:[],
	3:[4,5,6],
	4:[7],
	5:[],
	6:[8,9],
	7:[],
	8:[],
	9:[]
	}

	print(invertdict(ptodex))

	print(nodedist(extree,7,8))
	print(nodedist(extree,1,1))

	print(allnodedists(extree))

if __name__ == "__main__":
	runOld()
