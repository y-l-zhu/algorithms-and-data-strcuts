import sys, time, random, heapq
from math import ceil, log, sqrt
import numpy as np
from datetime import timedelta
import queue
from collections import defaultdict

random.seed(11)

def euclidean_distance(v1, v2):
	assert  len(v1) == len(v2)
	return sqrt(sum(list(map(lambda x,y: (x-y)**2, v1, v2))))


# @profile
def random_graph(vert, dim):

	result = [x[:] for x in [[-1] * vert] * vert]

	if dim == 0:
		for i in range(len(result)-1):
			for j in range(i+1, len(result)):
				dist = round(random.uniform(0, 1),8)
				result[i][j] = dist
				result[j][i] = dist

	else:
		axes = []
		if dim == 2:
			for i in range(vert):
				axes.append((random.uniform(0, 1), random.uniform(0, 1)))

		elif dim == 3:
			for i in range(vert):
				axes.append((random.uniform(0, 1),random.uniform(0, 1), random.uniform(0, 1)))

		elif dim == 4:
			for i in range(vert):
				axes.append((random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1), random.uniform(0, 1)))

		for i in range(len(result)-1):
			for j in range(i+1, len(result)):
				# if i != j:
				dist = round(euclidean_distance(axes[i], axes[j]), 8)
				result[i][j] = dist
				result[j][i] = dist

	return result


#@profile
def prim(G,s):
	"""
	For now, only support dim=2
	:return: MST
	"""
	nodes = len(G[0])
	dist = defaultdict(lambda: 10000)
	dist[s] = 0
	prev = defaultdict(lambda: None)

	S = [s]
	# X = []
	H = []
	heapq.heappush(H, (dist[s], s))
	while H != []:
		v = heapq.heappop(H)[1]
		# if (v, prev[v]) not in X:
		# 	X.append((v, prev[v]))
		if v not in S:
			S.append(v)
		for w in set(list(range(nodes))) - set(S):
			weight = G[v][w]
			if 0 < weight < thresh:
				if dist[w] > weight:
					dist[w] = weight
					prev[w] = v
					heapq.heappush(H, (dist[w], w))

	max_edge = max(dist.values())
	# print(max_edge)
	return sum(dist.values()), max_edge


if __name__ == "__main__":
	mode = int(sys.argv[1])
	num_points = int(sys.argv[2])
	num_trials = int(sys.argv[3])
	dimension = int(sys.argv[4])

	if dimension == 0:
		thresh = 0.01
	elif dimension == 2:
		thresh = 0.1
	elif dimension == 3:
		thresh = 0.2
	else:
		thresh = 0.3

	if num_points <= 512:
		thresh = 1


	G_weights = []
	G_max_edge = []

	for trial in range(num_trials):

		start_time = time.time()

		G = random_graph(num_points, dimension)
		s = 0
		weight, max_edge = prim(G, s)
		G_weights.append(weight)
		G_max_edge.append(max_edge)


	assert len(G_weights) == num_trials
	avr = sum(G_weights) / num_trials

	print()
	print(max(G_max_edge))
	print(avr)
	print(time.time() - start_time)
