import numpy as np
import time

# Build indices
nQ = 140
norb = 70
nocc = 20

# Build fake tensors
Qpq = np.random.random((nQ, norb, norb))
Cocc = np.random.random((norb, nocc))
D = np.dot(Cocc, Cocc.T)


# J = pqQ, Qrs, rs -> pq
# N^5 J algorithm
t = time.time()
J_n5 = np.einsum('Qpq,Qrs,rs->pq', Qpq, Qpq, D)
print('The N^5 J algorithm took      %10.6f seconds.' % (time.time() - t))


# N^3 J algorithm
t = time.time()
tmp1 = np.einsum('Qrs,rs->Q', Qpq, D)
J_n3 = np.einsum('Qpq,Q->pq', Qpq, tmp1)
print('The N^3 J algorithm took      %10.6f seconds. Correct? %s' %\
                (time.time() - t, np.allclose(J_n3, J_n5)))

# N^3 J with BLAS
t = time.time()
# Contraction 'Qrs,rs->Q' with GEMV compound indices ij,j->i
tmp1 = np.dot(Qpq.reshape(nQ, norb * norb), D.reshape(norb * norb))
# Contraction 'Qps,Q->ps' with GEMV compound indices i,ij->j
J_n3_BLAS = np.dot(tmp1, Qpq.reshape(nQ, norb * norb)).reshape(norb, norb)
print('The N^3 J BLAS algorithm took %10.6f seconds. Correct? %s' %\
                (time.time() - t, np.allclose(J_n3_BLAS, J_n5)))

print('\nNow for K algorithms')

# K = prQ, Qqs, rs -> pq
# N^5 K algorithm
t = time.time()
K_n5 = np.einsum('Qrp,Qqs,rs->pq', Qpq, Qpq, D)
print('The N^5 K algorithm took      %10.6f seconds' % (time.time() - t))


# N^4 K algorithm
t = time.time()
tmp1 = np.einsum('Qqs,rs->Qqr', Qpq, D)
K_n4 = np.einsum('Qrp,Qqr -> pq', Qpq, tmp1)
print('The N^4 K algorithm took      %10.6f seconds. Correct? %s' %\
                (time.time() - t, np.allclose(K_n5, K_n4)))

# N^4 K BLAS algorithm
t = time.time()
tmp1 = np.dot(Qpq.reshape(-1, norb), D.T).reshape(Qpq.shape)
tmp1 = np.einsum('Qir->Qri', tmp1)
K_n4_BLAS = np.dot(Qpq.reshape(nQ * norb, norb).T, tmp1.reshape(-1, norb))
print('The N^4 K BLAS algorithm took %10.6f seconds. Correct? %s' %\
                (time.time() - t, np.allclose(K_n5, K_n4_BLAS)))



