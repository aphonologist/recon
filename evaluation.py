def eval(gold, test):
	numbersharednodes = 0.0
	for node in gold:
		if node in tested:
			numbersharednodes += 1
	precision = numbersharednodes / len(test)
	recall = numbersharednodes / len(gold)
	fscore = 2 * precision * recall / (precision + recall)
	return [precision, recall, fscore]
