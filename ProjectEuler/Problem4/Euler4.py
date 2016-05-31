#author: Mike Zott
import numpy as np
import time

t= time.time()
nums = []
for i in range(100,1000):
    for j in range(100,1000):
        nums.append(str(i*j))
pals = []
for word in nums:
    if word[0] == word[-1] and word[1] == word[-2] and word[2] == word[-3]:
        pals.append(word)
pals = np.array(pals, dtype=int)
print pals
print max(pals)
print time.time()-t
