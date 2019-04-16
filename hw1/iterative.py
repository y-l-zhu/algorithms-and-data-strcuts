import time
import math

def fibonacci(n):
	A = []
	A.append(0)
	A.append(1)
	for i in range(2, n+1):
		A.append(A[i-1] + A[i-2])
	return A[n]


if __name__ == "__main__":
	t_end = time.time() + 60
	count = 0
	while time.time() < t_end:
		fib = fibonacci(count)
		count += 1
	print(count)
	print(fib % 65536)