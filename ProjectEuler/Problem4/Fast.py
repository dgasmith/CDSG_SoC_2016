print ("Problem 4: Largest Palindrome Product")
import time

print ("Speed up algorithm by counting backwards and never checking same product twice")

start = time.time()
def is_palidrome(n):
    f = str(n)
    if f[0] == f[-1] and f[1] == f[-2] and f[2] == f[-3]:
        return True
    else:
        return False

a = 999
answer = 0
while a >= 100:
    b = 999
    while b >= a:
        if a*b <= answer:
            break
        if is_palidrome(a*b):
            answer = a*b
        b -= 1
    a -= 1

print ("Answer: %d" % answer)
print ("Runtime: %6.6f" % (time.time() - start))

