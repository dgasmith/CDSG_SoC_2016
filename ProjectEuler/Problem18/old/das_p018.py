import time
import numpy as np

t_0 = time.time()

pt = np.loadtxt('padded_tri.txt')

for i in xrange(15):
	for j in xrange(np.count_nonzero(pt[i]) - 1):
		if pt[i, j] >= pt[i, j+1]:
			pt[i+1, j] += pt[i, j]
		else:
			pt[i+1, j] += pt[i, j+1]

print ("Answer: %d" % pt[14][0])
print ("Runtime: %6.6f" % (time.time() - t_0))                
