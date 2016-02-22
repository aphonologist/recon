import random

class Family:
	def __init__(self, rootlang):
		self.root = rootlang
		self.ranking = {self.root:[]}

	def evolve(self, l, p):
		
