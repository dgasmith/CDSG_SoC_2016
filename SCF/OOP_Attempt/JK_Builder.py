#Class definitions for JK BUilder
import numpy as np
import scipy.linalg.blas as blas

class JK_Builder:

    def __init__(self):
        self.nothing = "well shit" #Does JK_Builder need attributes??

    def build_DFJK(self, Qpq, Cleft, Cright = None):
        
        s = np.shape(Qpq)
        c = np.shape(Cleft)
        
        zeta1 = np.zeros((s[0] * s[1], c[1]))
        zeta2 = np.zeros((s[0], c[1], s[1]))
        
        if Cright is None: #Cij == Cik
            #K Construction: O(pN^2Naux) using orbital matrix
            np.dot(Qpq.reshape(s[0] * s[1], s[1]), Cleft, out=zeta1)
            np.einsum('Qpi->Qip', zeta1.reshape(s[0], s[1], c[1]), out=zeta2)
            zeta2.shape = (s[0] * c[1], s[1])
            K = np.dot(zeta2.T, zeta2)

            D_ = np.dot(Cleft, Cleft.T)

        elif not np.allclose(Cleft, Cright): #Cij != Cik
            left = np.shape(Cleft)
            right = np.shape(Cright)

            if left[1] == right[1]:
                D_ = np.dot(Cleft, Cright.T)

                zeta2.shape = (s[0] * s[1], c[1])
                np.dot(Qpq.reshape(s[0] * s[1], s[1]), Cleft, out=zeta1)

                np.dot(Qpq.reshape(s[0] * s[1], s[1]), Cright, out=zeta2)
                zeta1 = zeta1.reshape(s[0], s[1], c[1])
                zeta2 = zeta2.reshape(s[0], s[1], c[1])

                zeta1 = np.einsum('Qpi->Qip', zeta1)
                zeta2 = np.einsum('Qpi->Qip', zeta2)

                zeta1 = zeta1.reshape(s[0] * c[1], s[1])
                zeta2 = zeta2.reshape(s[0] * c[1], s[1])
                K = np.dot(zeta1.T, zeta2)

            else:
                raise Exception("C matrices cannot be contracted: Cleft dim 1 (%d) != Cright.T dim 0 (%d)" % (left[1], right[1]))
        else:
            raise Exception("Cright specified unecessarily")

        #J Construction: O(N^3)
        tmp = np.dot(Qpq.reshape(s[0],s[1]*s[2]),D_.reshape(s[1]*s[2]))
        J = np.dot(tmp,Qpq.reshape(s[0],s[1]*s[2])).reshape(s[1],s[2])

        return J, K
