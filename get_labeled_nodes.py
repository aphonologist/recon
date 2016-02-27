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
				tempnodes.add(str(temp))
		nodes.append(tempnodes)
	# remove any duplicates from list
	# duplicates come from branches like L-L-L-L-...-L with only one child
	outnodes = []
	for node in nodes:
		if node not in outnodes:
			if len(node) > 1:
				outnodes.append(node)
	return outnodes
