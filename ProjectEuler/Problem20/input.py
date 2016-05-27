print ("Problem 20")

import time

start = time.time()
n = 1

for j in range(1,101):
    n *= j

s = 0

while(n > 0):
    s += n%10
    n /= 10


print s
print ("Process took %6.6f seconds" % (time.time() - start))
