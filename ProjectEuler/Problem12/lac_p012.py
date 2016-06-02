import os,sys
sys.path.append('../')
from PyEuler import primes as pr
from PyEuler import factorize as fac
import numpy as np
import time

t = time.time()
prime_list = pr.sieve_erat(4000000)
n = 1
s = n*(n+1)/2
while (fac.number_divisors(fac.multiplicity(fac.factorize(s,prime_list)))<500):
	n+=1
	s = n*(n+1)/2
print s	
print ("This program takes %f s" %(time.time()-t))
