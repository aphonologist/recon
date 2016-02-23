import random, copy
from language import Language

class Family:
	def __init__(self, rootlang):
		self.languages = {rootlang:[]}

	def evolve(self, l, p):
		while self.count_leaves() < l:
			newlanguages = []
			for language in self.languages:
				r = random.random()
				if r <= p:
					# Copy the language
					# Note: two copies are made to avoid L1 - L2 - L3 - L4 ... - Ln trees
					newrank = copy.deepcopy(language.ranking)
					newname1 = str(len(self.languages) + 1)
					newname2 = str(len(self.languages) + 2)
					newlanguage1 = Language(language.constraints, newrank, newname1)
					newlanguage2 = Language(language.constraints, newrank, newname2)
					self.languages[language].append(newlanguage1)
					self.languages[language].append(newlanguage2)
					newlanguages.append(newlanguage1)
					newlanguages.append(newlanguage2)
				else:
					# Change the language if it does not have any children
					if not self.languages[language]:
						language.tweak_ranking()
			for newlanguage in newlanguages:
				self.languages[newlanguage] = []
	
	def count_leaves(self):
		count = 0
		for language in self.languages:
			if not self.languages[language]:
				count += 1
		return count

	def get_leaves(self):
		leaves = []
		for language in self.languages:
			if not self.languages[language]:
				leaves.append(language)
		return sorted(leaves, key=lambda language: language.__name__)
