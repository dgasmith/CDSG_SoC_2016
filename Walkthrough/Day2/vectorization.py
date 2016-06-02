import numpy as np
import time

# Reading materials:
# https://docs.scipy.org/doc/numpy-dev/user/quickstart.html
# http://www.valeevgroup.chem.vt.edu/docs/Intro2ComputerArchitecture4ComputationalScientists_2015.pdf

# Build two 3x3 NumPy matrices
A = np.random.random((3, 3))
B = np.random.random((3, 3))


# Cij = Aik * Bkj
# Simple matrix-matrix multiplication routine
def mmult(A, B):
    # Check shapes
    if A.shape[1] != B.shape[0]:
        raise ValueError("Zip shapes do not match!")
    
    # Build output
    C = np.zeros((A.shape[0], B.shape[1]))

    # Loop over it!    
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                C[i, j] += A[i, k] * B[k, j]
    return C


ret_mmult = mmult(A, B)
print 'mmult(A, B)'
print ret_mmult

# Check a few values by slicing
print 'A[0] * B.T[0]', np.sum(A[0] * B.T[0])
print 'A[0] * B[:, 0]', np.sum(A[0] * B[:, 0])
#print 'A[3] * B[0]', np.sum(A[3], B[0])
print '\n' + '-' * 30


# Broadcasting
a = np.random.random((3))
b = np.random.random((2))

print 'a', a
print 'b', b

# IndexError: Sizes do not match
#print a * b

a[:2] *= b
print 'a[:2] * b', a

a = a.reshape(3, 1)
print '\na.reshape(3, 1)'
print a

print 'a.shape', a.shape
print 'b.shape', b.shape

# Note that we can now "broadcast" 
print 'a * b'
print a * b

print '(a * b).shape', (a * b).shape

# Cikj = Aik * Bkj -> Cij
def vectorize_mmult(A, B):
    A = A.reshape(A.shape[0], A.shape[1], 1)
    return np.sum(A * B, axis=1)

print '\n' + '-' * 30

# The einsum function, http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.einsum.html
def einsum_mmult(A, B):
    # Cij = Aik * Bkj
    return np.einsum('ik,kj->ij', A, B)

# The np.dot version
np.dot(A, B)

A = np.random.random((300, 300))
B = np.random.random((300, 300))

t = time.time()
mmult(A, B)
print('mmult took           %20.3f us' % ((time.time() - t) * 1e6))

t = time.time()
vectorize_mmult(A, B)
print('vectorize_mmult took %20.3f us' % ((time.time() - t) * 1e6))

t = time.time()
einsum_mmult(A, B)
print('einsum_mmult took    %20.3f us' % ((time.time() - t) * 1e6))

# Need to init a few things, for full timings
# Do a quick trial run
np.dot(A, B)

t = time.time()
np.dot(A, B)
print('np.dot (BLAS) took   %20.3f us' % ((time.time() - t) * 1e6))

