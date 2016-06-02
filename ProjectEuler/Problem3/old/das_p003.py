import numpy as np
import time
import sys
sys.path.append('../../')
import PyEuler.primes as pr
import PyEuler.factorize as fact

t_0 = time.time()

num = 600851475143
prime_list = pr.sieve_erat(int(num**0.5))
factor_list = fact.factorize(num, prime_list)

print('Maximum factor of %d is %d' % (num, max(factor_list)))
print('Runtime: %6.6f' % (time.time() - t_0))
