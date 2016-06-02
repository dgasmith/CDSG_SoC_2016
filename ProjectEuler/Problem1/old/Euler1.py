#author: Mike Zott
import time

t= time.time()
answer = 0
for i in range(1,1000):
    if(i%3 == 0 or i%5 == 0):
        answer+=i
print answer
print time.time()-t
