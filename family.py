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
					newrank = copy.deepcopy(language.ranking)
					newname = str(len(self.languages) + int(language.__name__) + 1)
					newlanguage = Language(language.constraints, newrank, newname)
					self.languages[language].append(newlanguage)
					newlanguages.append(newlanguage)
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
		return leaves
