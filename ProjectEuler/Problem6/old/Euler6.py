#author: Mike Zott
import numpy as np
import time

t = time.time()
nums = np.array(range(1,101))
nums = nums * nums

print  sum(range(1,101)) **2 - sum(nums)
print time.time() - t
