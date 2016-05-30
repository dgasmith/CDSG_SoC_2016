import time
import math

start = time.time()

print ("Problem 7: Using Trial Division to Check for Primality")

count = 2
test = 3

while (count < 10001 ):
    flag = 1
    test += 2
    for j in range(2, int(math.sqrt(test)) + 1):
        if(test % j==0):
            flag = 0
            break
    if(flag==1):
        count +=1


print("The 10001st  prime number is %d" % test)
print("Runtime: %6.3f" % (time.time() - start))

