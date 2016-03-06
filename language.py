import random, copy

class Language:
	def __init__(self, constraints, ranking=None, name=1):
		self.constraints = constraints
		# Ranking: digraph stored as adjacency list
		self.c = len(constraints)
		if not ranking:
			self.ranking = {constraint:{} for constraint in self.constraints}
		else:
			self.ranking = ranking
		self.__name__ = name
		self.normalized_ranking = []
		self.length = 0.0

	def __str__(self):
		return self.__name__

	def __repr__(self):
		return str(self.__name__)

	def randomize_ranking(self):
		# Fully, randomly rank the constraint set
		shuffled = self.constraints[:]
		random.shuffle(shuffled)
		for i in range(self.c - 1):
			self.ranking[shuffled[i]][shuffled[i+1]] = {}

	def get_pairwise(self):
		# Get pairwise comparison vector; 1 if a >> b, -1 if b >> a, 0 if no relation
		self.pairwise_ranking = []
#		sorted_constraints = sorted(self.constraints)
		for c1 in range(self.c):
			for c2 in range(self.c):
				rank = self.search_rank(self.constraints[c1], self.constraints[c2])
				self.pairwise_ranking.append(rank)

	def search_rank(self, c1, c2):
		if not self.ranking[c1]:
			return 0
		if c2 in self.ranking[c1]:
			return 1
		else:
			for c3 in self.ranking[c1]:
				if self.search_rank(c3, c2) == 1:
					return 1
		return 0

	def normalize_ranking(self):
		self.get_pairwise()
		# Get length of vector: square root of sum of squares of values
		for p in self.pairwise_ranking:
			self.length += p**2
		self.length **= .5
		if self.length == 0.0:
			self.length = 1.0
		# Divide each entry in pairwise vector by the length of the vector
		self.normalized_ranking = [p/self.length for p in self.pairwise_ranking]

	def tweak_ranking(self):
		# Randomly modify ranking
		r = random.random()
		if r < .5:
			# Remove a link
			r1 = random.randint(0, self.c - 1)
			constraint = self.constraints[r1]
			if self.ranking[constraint]:
				self.ranking[constraint].popitem()
		else:
			# Add a link
			r1 = random.randint(0, self.c - 1)
			r2 = random.randint(0, self.c - 1)
			if r1 != r2: # constraints cannot dominate themselves
				con1 = self.constraints[r1]
				con2 = self.constraints[r2]
				if self.search_rank(con2, con1) + self.search_rank(con1, con2) == 0:
					# make sure this will not create a loop
					self.ranking[con1][con2] = {}
