import time

max_value = int(1e7)

t = time.time()
result = 0
for num in range(max_value):
    if ((num % 3) == 0) or ((num % 5) == 0):
        result += num

print("The answer to problem 1 is %d" % result)
print("Total time taken %3.3f" % (time.time() - t))
