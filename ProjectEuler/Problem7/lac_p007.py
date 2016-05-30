import time
import numpy as np
import math

t = time.time()

def isprime(number):
  prime = True;
  if number%2==0:
    prime = False
  else:
    for i in range(3,int(math.ceil(math.sqrt(number)))+1,2):
      if (number%i==0):
        prime = False
        break
  return prime

number = np.arange(3,2000000)
prime_pos = 2
for element in number:
  if (isprime(element)):
     prime_pos+=1
     aux = element
  if (prime_pos>10001):
     break
  
      

print aux
print ("This program takes %f s" %(time.time()-t))
