import time

t = time.time()
n = 100
#Sum of Arithmetic Progression: Sn = n*(n+1)/2
#Sum of Squares: Sn = n*(n+1)*(2n+1)/6

diff = n*(n+1)*(3*n*n-n-2)/12
print diff
print ("This program takes %f s" % (time.time()-t))
