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
print max(pals)
print time.time()-t

"""Notes:  
- This is the fastest way to check is_Palidrome and is used in the Fast.py.  
- There is no need to create nums (could have just used the for loops directly).
  Although saving them linearly rather than in 2D may have been benificial here.
- It is not necessary to save every palidrome.  We can just save the largest.
- The largest slowdown is due to checking every number i*j(created by the above loops).
This leades to checking multiple numbers twice.  Also, checking down from 999*999 
and stopping after the largest palidrome is the greatest speedup."""
