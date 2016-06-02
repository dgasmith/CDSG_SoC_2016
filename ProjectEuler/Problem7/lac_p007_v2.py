import os,sys
sys.path.append('../')
from PyEuler import primes as pr
import numpy as np

upper_lim = 4000000;
print pr.sieve_erat(upper_lim)[10000]

