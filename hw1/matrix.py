import time
import math

def multi_matrix(a, b):
	c = [[0 for row in range(len(b[0]))] for col in range(len(a))]
	for row_a in range(len(a)):
		for col_b in range(len(b[0])):
			for col_a in range(len(a[0])):
				c[row_a][col_b] += a[row_a][col_a] * b[col_a][col_b]
	return c


def fibonacci(n):
	A = [[0, 1], [1, 1]]
	f_0 = 0
	f_1 = 1
	f_n = [[0, 1], [1, 1]]
	if n == 0:
		return f_0
	elif n == 1:
		return f_1
	else:
		for i in range(1, int(math.log(n, 2))):
			A = multi_matrix(A, A)
		return multi_matrix(A, [[f_0], [f_1]])[0][0]


if __name__ == "__main__":
	t_end = time.time() + 60
	count = 0
	while time.time() < t_end:
		fib = fibonacci(count)
		count += 1
	print(count)
	print(fib % 65536)
