def eval(gold, test):
	numbersharednodes = 0.0
	for node in gold:
		if node in test:
			numbersharednodes += 1.0
	precision = numbersharednodes / len(test)
	recall = numbersharednodes / len(gold)
	fscore = 2 * precision * recall
	if fscore > 0:
		fscore /= (precision + recall)
	return [precision, recall, fscore]
