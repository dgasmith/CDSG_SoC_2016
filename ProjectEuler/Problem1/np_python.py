import time
import numpy as np

max_value = int(1e8)

arr = np.arange(max_value)
t = time.time()
result = np.sum(arr[((arr % 3) == 0) | ((arr % 5) == 0)])
print("The numpy result is %d" % result)
print("total time taken %3.3f" % (time.time() - t))



