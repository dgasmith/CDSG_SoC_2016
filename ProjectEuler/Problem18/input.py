print "Problem 18: Maximum Path Sum: Bottom-Up Approach"
import time
start = time.time()
f = open('path.txt')

i = 0
arr = []

for line in f:
    s = line[1:]
    arr.append([])
    while len(s) > 3:
        arr[i].append(int(s[0:2]))
        s = s[3:]
    arr[i].append(int(s[0:2]))
    i += 1
f.close()
  
i = len(arr) - 2
while i >= 0:
    j = 0
    while j < len(arr[i]):
        left = arr[i+1][j]
        right = arr[i+1][j+1]
        if left > right:
            arr[i][j] += left
        else:
            arr[i][j] += right
        j += 1
    i -= 1

print ("Answer: %d" % arr[0][0])
print ("Runtime: %6.6f" % (time.time() - start))                
