import os,sys
sys.path.append('../')
from PyEuler import fibo
import numpy as np

seq = np.array([1,2])
while seq[-1]<4000000:
	seq = fibo.fibo(seq)
print np.sum(seq[1::3])
