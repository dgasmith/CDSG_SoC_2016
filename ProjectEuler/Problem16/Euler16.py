import numpy as np
import time

t = time.time()

nums = []
num = 2**1000
num = str(num)
for i in range(len(num)):
    nums.append(num[i])
    nums[i] = int(nums[i])
print sum(nums)
print time.time()-t

