def get_nodes(tree):
	# Returns a set of sets of nodes dominated by each internal node in a tree
	nodes = set([])
	for node in tree:
		stack = set([node])
		tempnodes = set([])
		while stack:
			temp = stack.pop()
			if not tree[temp]:
				tempnodes.add(temp)
			else:
				for t in tree[temp]:
					stack.add(t)
		nodes.add(tempnodes)
	return nodes
