import numpy as np
import time

t = time.time()
x = np.arange(100,1000)
y = np.outer(x,x)
pal = False
element = 0
for m in range(x.size):
  for n in range(m):
    e = str(y[m,n])
    tam = len(e)
    for i in range((tam-1)/2+1):
      if e[i]!=e[tam-1-i]:
         pal=False
         break
      else:
         pal = True
    if pal:
     if y[m,n] > element:
       element = y[m,n]
print element
print ("Time to run the program is: %f" % (time.time()-t))
