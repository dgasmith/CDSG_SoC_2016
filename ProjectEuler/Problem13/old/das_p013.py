import numpy as np
import time

t_0 = time.time()
print(np.sum(np.loadtxt('das_p013.txt'))) # Read numbers into numpy array, and add them
print("Time: %f" % (time.time()-t_0))
