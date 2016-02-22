import random

class Language:
	def __init__(self, constraints):
		self.constraints = constraints
		# Ranking: digraph stored as adjacency list
		self.c = len(constraints)
		self.ranking = {constraint:[] for constraint in self.constraints}

	def randomize_ranking(self):
		# Fully, randomly rank the constraint set
		random.shuffle(self.constraints)
		for i in range(self.c - 1):
			self.ranking[self.constraints[i]].append(self.constraints[i+1])

	def check_for_loops(self):
		G = self.ranking
		color = {u:'white' for u in G}
		found_cycle = False
		for u in G:
			if color[u] == 'white':
				self.dfs_visit(G, u, color, found_cycle)
			if found_cycle:
				break
		return found_cycle
	
	def dfs_visit(self, G, u, color, found_cycle):
		if found_cycle:
			return
		color[u] = 'gray'
		for v in G[u]:
			if color[v] == 'gray':
				found_cycle = True
				return
			if color[v] == 'white':
				self.dfs_visit(G, v, color, found_cycle)
		color[u] = 'black'
