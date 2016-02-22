import random

class Family:
	def __init__(self, rootlang):
		self.root = rootlang
		self.languages = {self.root:[]}

	def evolve(self, l, p):
		while self.count_leaves() < l:
			newlang = str(len(self.languages) + 1)
			self.languages[newlang] = []
	
	def count_leaves(self):
		count = 0
		for language in self.languages:
			if not self.languages[language]:
				count += 1
		return count
