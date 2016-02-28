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
					# Copy the language but be a binary tree
					if not self.languages[language]:
						newrank1 = copy.deepcopy(language.ranking)
						newrank2 = copy.deepcopy(language.ranking)
						newname1 = str(len(self.languages) + int(language.__name__) + 1)
						newname2 = str(len(self.languages) + int(language.__name__) + 2)
						newlanguage1 = Language(language.constraints, newrank1, newname1)
						newlanguage2 = Language(language.constraints, newrank2, newname2)
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
		return leaves

	def tree_to_dot(self, name='temp_tree'):
		out = 'digraph family {\n'
		for l1 in self.languages:
			for l2 in self.languages[l1]:
				out += '\t' + l1.__name__ + '->' + l2.__name__ + ';\n'
		out += '}'
		f = open(name+'.dot', 'w')
		f.write(out)
		f.close()
