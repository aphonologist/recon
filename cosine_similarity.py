def cosine(v1, v2):
	return dot_product(v1,v2) / (v1.length * v2.length)

def dot_product(v1, v2):
	sum = 0
	for i in range(len(v1.normalized_ranking)):
		sum += v1.normalized_ranking[i] * v2.normalized_ranking[i]
	return sum
