"Module containing functions useful for handline prime numbers."

import numpy as np

def sieve_erat(num):
	"""Returns list of all primes between integers smaller than *num*.

	Parameters:
		integer *num* -- Upper bound for prime searching
	
	Return:
		list *primes* -- List of all prime numbers in range(low, high)
		Note: if no primes, returns empty list.
	Algorithm:
		Sieve of Eratosthenes"""
	sieve = np.ones(num + 1)
	sieve[:2] = 0
	for x in xrange(2, int(np.sqrt(num)) + 1):
		sieve[x**2::x] = 0

	return np.nonzero(sieve)[0]

 
