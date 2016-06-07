#!/home/dasirianni/miniconda2/bin/python

first = 1
second = 2

n_1 = second
n_2 = first
n = n_1 + n_2

total = 2

while n <= 4000000:
	if n % 2 == 0:
		total += n
	n = n_2 + n_1
	n_2 = n_1
	n_1 = n

print total
