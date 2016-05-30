print ("Problem 14: Non-Redundant Approach")
import time
start = time.time()

max_number = int(1e6)

s = [1]*max_number
answer = 1

for j in range(1,max_number):
    count = 1
    n = j
    while n > 1:
        if n < j:
            count += s[n-1]-1
            break       
        if n%2 == 0:
            n /= 2
            count += 1
        else:
            n = 3*n +1
            count += 1
    if count > s[answer-1]:        
        answer = j
    s[j-1] = count
        
print ("Answer: %d" %answer)
print ("Runtime: %6.3f" % (time.time() - start))
