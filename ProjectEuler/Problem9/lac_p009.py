import numpy as np
import time
import math

# Manipulating a^2+b^2=c^2 and a+b+c=1000 -> abc = c*(500000-1000c)  --> c<500
# Manipulating everything: a = (1000-c+sqrt(c^2+2000*c-1000000))/4
#                          b = (1000-c-sqrt(c^2+2000*c-1000000))/4
# The argument of the sqrt has to be a perfect square -> c^2+2000*c-1000000 = m^2

t = time.time()
square = []
for m in range(48,497):
  square.append(m*m)
for c in range(415,500):
  aux = c*c+2000*c-1000000
  for j in range(len(square)):
    if square[j] == aux:
      a = (1000-c+math.sqrt(aux))/2
      b = (1000-c-math.sqrt(aux))/2
      prod = a*b*c
      print prod
print ("This program takes %f s" % (time.time()-t))
