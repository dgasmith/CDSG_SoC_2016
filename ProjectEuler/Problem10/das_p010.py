import os, sys
sys.path.append('../')
from PyEuler import primes as pr
import numpy as np

print np.sum(pr.sieve_erat(2000000))
