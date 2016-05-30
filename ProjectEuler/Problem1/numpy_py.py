import time
import numpy as np

max_value = int(1e6)

arr = np.arange(max_value)
t = time.time()
print arr % 3 == 0
print np.sum(arr[((arr % 3) == 0) | ((arr % 5) == 0)])
print("Total time taken %3.3f" % (time.time() - t))
