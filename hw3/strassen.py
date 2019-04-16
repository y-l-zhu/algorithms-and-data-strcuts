import sys, time, random
from math import ceil, log
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt


def load_matrix(f, d):
	matrix = []
	row = []
	for n in f:
		if number_type == "float":
			n = float(n.strip())
		else:
			n = int(n.strip())
		row.append(n)
		if len(row) == d:
			matrix.append(row)
			row = []
	return matrix


def naive_multiply(A, B):
	"""
	input: two n*n matrices (list of lists) A and B
	output: result of naive multiplication of order O(n^3)
	"""
	assert len(A) == len(B)
	if number_type == "float":
		result = [x[:] for x in [[0.0] * len(A)] * len(A)]
	else:
		result = [x[:] for x in [[0] * len(A)] * len(A)]
	for i in range(len(A)):
		for j in range(len(B[0])):
			for k in range(len(B)):
				result[i][j] += A[i][k] * B[k][j]
	return result


def naive_opt(A, B, if_add):
	assert len(A) == len(A[0]) == len(B) == len(B[0])
	if number_type == "float":
		result = [x[:] for x in [[0.0] * len(A)] * len(A)]
	else:
		result = [x[:] for x in [[0] * len(A)] * len(A)]
	for i in range(len(A)):
		for j in range(len(A[0])):
			if if_add:
				result[i][j] = A[i][j] + B[i][j]
			else:
				result[i][j] = A[i][j] - B[i][j]
	return result


def concat(C11, C12, C21, C22):
	assert len(C11) == len(C12) == len(C21) == len(C22) == len(C11[0]) == len(C21[0]) == len(C21[0]) == len(C22[0])
	result = []
	for i in range(len(C11)):
		result.append(C11[i]+C12[i])
	for i in range(len(C21)):
		result.append(C21[i]+C22[i])
	return result


def pad_zeros(M, dim):
	"""
	input: 	M:   the matrix to pad zeros
			dim: the desired matrix dimension
	output: M with padded zeros
	"""
	assert len(M)>=1
	if len(M) == dim and len(M[0]) == dim:
		return M
	else:
		if number_type == "float":
			result = [x[:] for x in [[0.0] * dim] * dim]
		else:
			result = [x[:] for x in [[0] * dim] * dim]

		for i in range(len(M)):
			for j in range(len(M[0])):
				try:
					result[i][j] = M[i][j]
				except:
					pass
		return result


def round_matrix(M, precision):
	for i in range(len(M)):
		for j in range(len(M[0])):
			M[i][j] = round(M[i][j], precision)
	return M


def strassen(A, B):
	assert len(A) == len(B)
	assert len(A[0]) == len(B[0])
	assert len(A) == len(A[0])
	d = len(A)

	if d <= edge:
		C = naive_multiply(A, B)

	else:
		n = 2* ceil(d/2)

		if d != n:
			A = pad_zeros(A, n)
			B = pad_zeros(B, n)

			# initialize matrix division
		A11 = [x[:(n//2)] for idx, x in enumerate(A) if idx<(n//2)]
		A12 = [x[(n//2):] for idx, x in enumerate(A) if idx<(n//2)]
		A21 = [x[:(n//2)] for idx, x in enumerate(A) if idx>=(n//2)]
		A22 = [x[(n//2):] for idx, x in enumerate(A) if idx>=(n//2)]
		B11 = [x[:(n//2)] for idx, x in enumerate(B) if idx<(n//2)]
		B12 = [x[(n//2):] for idx, x in enumerate(B) if idx<(n//2)]
		B21 = [x[:(n//2)] for idx, x in enumerate(B) if idx>=(n//2)]
		B22 = [x[(n//2):] for idx, x in enumerate(B) if idx>=(n//2)]

		P1 = strassen(A11, naive_opt(B12, B22, if_add=False))
		P2 = strassen(naive_opt(A11, A12, if_add=True), B22)
		P3 = strassen(naive_opt(A21, A22, if_add=True), B11)
		P4 = strassen(A22, naive_opt(B21, B11, if_add=False))
		P5 = strassen(naive_opt(A11, A22, if_add=True), naive_opt(B11, B22, if_add=True))
		P6 = strassen(naive_opt(A12, A22, if_add=False), naive_opt(B21, B22, if_add=True))
		P7 = strassen(naive_opt(A11, A21, if_add=False), naive_opt(B11, B12, if_add=True))

		C11 = naive_opt(naive_opt(naive_opt(P5, P4, if_add=True), P2, if_add=False), P6, if_add=True)
		C12 = naive_opt(P1, P2, if_add=True)
		C21 = naive_opt(P3, P4, if_add=True)
		C22 = naive_opt(naive_opt(naive_opt(P1, P5, if_add=True), P3, if_add=False), P7, if_add=False)

		C = concat(C11, C12, C21, C22)

		if d != n:
			C = pad_zeros(C, d)

	return C

if __name__ == "__main__":
	mode = sys.argv[1]
	d = int(sys.argv[2])
	file = sys.argv[3]
	global edge
	global number_type
	edge = 19


	start_time = time.time()

	if mode == "0":
		f = open(file, encoding='utf8').read()
		if "." in f:
			number_type = "float"
		else:
			number_type = "int"
		f = [x for x in f.split("\n") if x != '']
		half = len(f) // 2
		A = load_matrix(f[:half], d)
		B = load_matrix(f[half:], d)
		if d <= edge:
			edge = d
		C = round_matrix(strassen(A, B), 8)
		for n in range(d):
			print(C[n][n])


	elif mode != "4":
		random.seed(11)

		gen_matrix = []
		for n in range(2*d*d):
			gen_matrix.append(round(random.uniform(0, 1),8))
		gen_f = open(file, "w")
		for n in gen_matrix:
			gen_f.write("%2f\n" % n)
		gen_f.close()

		f = open(file, encoding='utf8').read()
		if "." in f:
			number_type = "float"
		else:
			number_type = "int"
		f = [x for x in f.split("\n") if x != '']
		half = len(f) // 2
		A = load_matrix(f[:half], d)
		B = load_matrix(f[half:], d)
		# print(A)
		# print(B)

		if mode == "1":
			C = round_matrix(strassen(A, B), 8)
			for line in C:
				print(line)

		if mode == "2":
			C = round_matrix(naive_multiply(A, B), 8)
			for line in C:
				print(line)

		elapsed = time.time() - start_time
		sys.stdout.write(str(timedelta(seconds=elapsed)) + "\n\n")

		if mode == "3":
			count_start_naive = time.time()
			naive_C = naive_multiply(A, B)
			count_elapsed_naive = time.time()-count_start_naive
			print("naive", count_elapsed_naive)
			for edge in range(2, 100):
				assert edge <= d
				count_start_time = time.time()
				C = strassen(A, B)
				count_elapsed = time.time() - count_start_time
				if count_elapsed < count_elapsed_naive:
					print("##### Fast #####")
					print(d, edge, count_elapsed)
					break

	elif mode == "4":
		optimal_f = open("optimal", "w")
		for d in range(128, 300):
			random.seed(11)

			gen_matrix = []
			for n in range(2*d*d):
				gen_matrix.append(round(random.uniform(0, 1),8))
			gen_f = open(file, "w")
			for n in gen_matrix:
				gen_f.write("%2f\n" % n)
			gen_f.close()

			f = open(file, encoding='utf8').read()
			if "." in f:
				number_type = "float"
			else:
				number_type = "int"
			f = [x for x in f.split("\n") if x != '']
			half = len(f) // 2
			A = load_matrix(f[:half], d)
			B = load_matrix(f[half:], d)


			print("#############")
			print(d)
			count_start_naive = time.time()
			naive_C = naive_multiply(A, B)
			count_elapsed_naive = time.time()-count_start_naive
			print("naive", count_elapsed_naive)

			for edge in range(4, 100):
				assert edge <= d
				count_start_time = time.time()
				C = strassen(A, B)
				count_elapsed = time.time() - count_start_time
				if count_elapsed < count_elapsed_naive:
					print("##### Fast #####")
					print(d, edge, count_elapsed)
					optimal_f.write("%d\t%d\t%f\n" % (d, edge, count_elapsed))
					break
		optimal_f.close()
