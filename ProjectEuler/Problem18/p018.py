import time
import numpy as np

t_0 = time.time()

pt = np.loadtxt('padded_tri.txt')

i = 0
while i < 15:
	nonzero = np.count_nonzero(pt[i]) - 1
	j = 0
	while j < nonzero:
		left = pt[i, j]
		right = pt[i, j+1]
		if left > right:
			pt[i+1, j] += left
		else:
			pt[i+1, j] += right
		j += 1
	i += 1

print (pt[14][0])
print ("Runtime: %6.6f" % (time.time() - t_0))                
