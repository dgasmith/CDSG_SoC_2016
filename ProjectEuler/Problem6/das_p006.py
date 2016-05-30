import numpy as np

print((np.sum(i for i in xrange(1,101)))**2 - np.sum(i**2 for i in xrange(1,101)))
