print ("Problem 14: Longest Collatz sequence under 1e6")

def Collatz_Length(n):
   length = 1
   while n > 1:
        if n%2==0:
            n /= 2
        else:
            n = 3*n + 1
        length += 1
   return length

import time
start = time.time()

longest = 1
num = 1

for j in range(1,1000001):
    temp = Collatz_Length(j)
    if temp > longest:
        longest = temp
        num = j

print ("Answer: %d" % num)

print ("Runtime: %6.3f" % (time.time() - start))
        
