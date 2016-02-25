def eval(gold, test):
	numbersharednodes = 0.0
	for node in gold:
		if node in test:
			numbersharednodes += 1
	precision = numbersharednodes / len(test)
	recall = numbersharednodes / len(gold)
	if precision + recall > 0:
		fscore = 2 * precision * recall / (precision + recall)
	else:
		fscore = 0
	return [precision, recall, fscore]
