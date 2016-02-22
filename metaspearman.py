def spearman(X, Y):
	n = len(X)
	items = sorted([x for x in X])
	rankX = [X.index(i) + 1 for i in items]
	rankY = [Y.index(i) + 1 for i in items]
	d = []
	for i in range(n):
		d.append(rankX[i] - rankY[i])
	d2 = [x**2 for x in d]
	sigma_d2 = 0
	for x in d2:
		sigma_d2 += x
	r = 1 - (6 * sigma_d2) / (n * (n**2 - 1))
	return r

f1 = open('dist_from_one_spear.txt')
l1 = []
for line in f1:
	l1.append(line.strip())	
f1.close()

f2 = open('dist_from_one_dist.txt')
l2 = []
for line in f2:
	l2.append(line.strip())
f2.close()

f3 = open('dist_from_one_euc.txt')
l3 = []
for line in f3:
	l3.append(line.strip())
f3.close()

f4 = open('dist_from_one_cos.txt')
l4 = []
for line in f4:
	l4.append(line.strip())
f4.close()

f5 = open('dist_from_one_ham.txt')
l5 = []
for line in f5:
	l5.append(line.strip())
f5.close()

output = open('stats.txt','a')

print('simple difference: ', spearman(l1,l2))
print('euclidean distance: ', spearman(l1,l3))
print('cosine similarity: ', spearman(l1,l4))
print('hamming distance: ', spearman(l1,l5))
output.write('simple difference: ' + str(spearman(l1,l2)))
output.write('\n')
output.write('euclidean distance: ' + str(spearman(l1,l3)))
output.write('\n')
output.write('cosine similarity: ' + str(spearman(l1,l4)))
output.write('\n')
output.write('hamming distance: ' + str(spearman(l1,l5)))
output.write('\n')
