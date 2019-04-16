import time
import math

def fibonacci(n):
	if n == 0:
		return 0
	elif n == 1:
		return 1
	else:
		return fibonacci(n-1) + fibonacci(n-2)


if __name__ == "__main__":
	t_end = time.time() + 60
	count = 0
	fib = 0
	while time.time() < t_end:
		fib = fibonacci(count)
		count += 1
	print(count)
	print(fib % 65536)
