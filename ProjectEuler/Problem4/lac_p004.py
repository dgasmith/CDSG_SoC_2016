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
        pal=True 
    if pal:
     if y[m,n] > element:
       element = y[m,n]
print element
print ("Time to run the program is: %f" % (time.time()-t))

"""Notes: 
- np.outer is good use of numpy library here.
- Checks for Palidromes quckly.
- Only checks half of the products (avoids duplicates).
- Saves only the largest palidrome (element).
- Not sure why this performs slower than Euler4.py.  Perhaps navigating
  the matrix y takes more time, since the products of Euler4.py were saved
  and scanned linearly.
- Greatest speedup would be to replace for loops with while loops and scan
  backwards, stopping after the greatest palidrome product is found.
""" 
