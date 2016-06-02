print ("Problem 16: High precision is great!")
import time
start = time.time()

b = 2**1000
s = 0

while b > 0:
    s += b%10
    b /= 10

print ("Answer: %d" % s)
print ("Runtime: %6.6f" % (time.time() - start)) 
