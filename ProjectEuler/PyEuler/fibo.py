" Module containing a generator of Fibonacci sequence list."
import numpy as np

def fibo(f_seq):
	"""Returns list of FIbonacci sequence elements.

	Parameters:
		list *f_seq* -- list of Fibonacci sequence elements already computed.

	Return:
		list of FIbonacci sequence elements """
	return np.append(f_seq,f_seq[-1]+f_seq[-2])

