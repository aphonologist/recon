def get_nodes(tree):
	# Returns a set of sets of leaves dominated by each internal node in a tree
	nodes = []
	for node in tree:
		stack = [node]
		tempnodes = set([])
		while stack:
			temp = stack.pop()
			if tree[temp]:
				for t in tree[temp]:
					stack.append(t)
			else:
				tempnodes.add(temp)
		nodes.append(tempnodes)
	return nodes
