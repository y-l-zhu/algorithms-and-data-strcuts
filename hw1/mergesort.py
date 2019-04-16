import sys

def merge_sort(A):
	if len(A) == 1:
		return A
	else:
		mid = len(A)//2
		l = merge_sort(A[:mid])
		r = merge_sort(A[mid:])
		merged = []
		i, j = 0, 0
		while i < len(l) and j < len(r):
			if l[i] < r[j]:
				merged.append(l[i])
				i += 1
			else:
				merged.append(r[j])
				j += 1
		merged += l[i:]
		merged += r[j:]
		return merged


if __name__ == "__main__":
	a = sys.stdin.readline()
	# data = [3, 7, 9, 14, 66, 34, 21, 25, 53]
	print(merge_sort(a))
