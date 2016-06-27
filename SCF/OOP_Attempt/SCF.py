#SCF Class definitions
import time
import numpy as np
import psi4
import scipy.linalg as sl
from JK_Builder import JK_Builder

class SCF:
    
    def __init__(self, wfn, dE_tol, dRMS_tol, maxmacro, SOSCF_tol, maxmicro):
        self.psi4 = psi4
        self.wfn = wfn
        self.dE_tol = dE_tol
        self.maxmacro = maxmacro
        self.dRMS_tol = dRMS_tol
        self.SOSCF_tol = SOSCF_tol
        self.maxmicro = maxmicro
        self.Mints = psi4.MintsHelper(self.wfn.basisset())
        self.S = np.asarray(self.Mints.ao_overlap())
        self.T = np.asarray(self.Mints.ao_kinetic())
        self.V = np.asarray(self.Mints.ao_potential())
        self.H = self.T + self.V
        del self.T, self.V
        self.JK = JK_Builder()
        self.Enuc = self.wfn.molecule().nuclear_repulsion_energy()
        self.ndocc = self.wfn.nalpha()
        self.nbf = self.S.shape[0]
        self.nvirt = self.nbf - self.ndocc
        self.microtime = 0.0
        self.totmicro = 0

    def diagonalize(self, F, A):
        Fp = np.dot(A.T,F).dot(A)
        eigval, eigvec = np.linalg.eigh(Fp)
        C = np.dot(A,eigvec)
        Cocc = C[:,:self.ndocc]
        Cvirt = C[:,self.ndocc:]
        D = np.einsum('pi,qi->pq',Cocc,Cocc)
        return C, Cocc, Cvirt, D
    
    def DIIS(self, trials, errors, F, r):

        trials.append(F)

        #Obtain DIIS error    
        if len(errors) > 8: #only keep the 8th most recent guesses for use.
            del errors[0]
            del trials[0]
        errors.append(r)

        #Build B
        size = len(errors) + 1
        B = np.zeros((size, size))
        B[-1] = -1
        B[:,-1] = -1
        B[-1,-1] = 0
        for i in range(size-1):
            for j in range(size-1):
                B[i,j] = np.sum(errors[i] * errors[j])

        #Solve for Cn
        vec = np.zeros(size)
        vec[-1] = -1
        inverse = np.linalg.inv(B)
        Cn = np.linalg.solve(B, vec)

        #Rebuild Fock Matrix according to Cn
        F = np.zeros_like(F)
        for i in range(len(Cn) - 1):
            F += Cn[i] * trials[i]

        return F
        #Diagonalize F and Reproduce Density Matrix after!!
    
    def SOSCF(self, C, F, Qpq, ndocc, nvirt):
        # Remember only the OV part is needed.
        grad = -4 * np.dot(C.T, F).dot(C)[:ndocc, ndocc:]
        Fmo = np.einsum('ij,jk,kl->il', C.T, F, C)         
        nrot = ndocc * nvirt       
       
             
        eps = np.diag(Fmo)
        precon = -4 * (eps[:ndocc][:, None] - eps[ndocc:])
        
        k = -grad / precon
        p = []
        rk = []
        z = []
        
        Cocc = C[:,:ndocc] 
        Cvirt = C[:,ndocc:]
        Ax = self.build_Ax(Fmo, Cocc, k, Cvirt, Qpq).ravel()
        
        k = k.ravel()
        rk.append(-grad.ravel() - Ax)
        z.append(rk[0]/precon.ravel())
        p.append(z[0])
        grad_rms = np.mean( grad ** 2) ** 0.5
        #rk and pk are column vectors! 
        microstart = time.time()
        for j in range(self.maxmicro):

            tmp = self.build_Ax(Fmo, Cocc, p[j].reshape(ndocc, nvirt), Cvirt, Qpq).ravel()                   

            alpha = np.dot(rk[j].T, z[j])
            alpha /= np.dot(p[j].T, tmp)
             
            k = k + alpha*p[j]
            rk.append(rk[j] - alpha*tmp)
             
            err = np.mean(rk[j+1]**2)**0.5
            err = err / grad_rms
            print ("SOSCF Microiteration %d: RMS = %2.5E" % (j+1, err))
            self.totmicro += 1 
            if err < self.SOSCF_tol or j == self.maxmicro - 1:
                if j == self.maxmicro - 1:
                    print ("SOSCF could not converge and was turned OFF\n")
                    soscf = False
                break

            z.append(rk[j+1]/precon.ravel())
            beta = np.dot(z[j+1].T, rk[j+1]) / np.dot(z[j].T,rk[j])
            p.append(z[j+1] + beta*p[j])

        self.microtime += (time.time() - microstart)
        # Convert back, mind the compound indices
        k.shape = (ndocc, nvirt)

        # Build the full Kappa matrix
        full_K = np.zeros((self.nbf, self.nbf))
        full_K[:ndocc, ndocc:] = k
        full_K[ndocc:, :ndocc] = -k.T
        # Construct U and new orbitals
        U = sl.expm(full_K)
        C = np.dot(C, U)
        # Update other matrices
        Cocc = C[:, :ndocc].copy()
        Cvirt = C[:, ndocc:].copy()
        D = np.dot(Cocc, Cocc.T)

        return C, Cocc, Cvirt, D, soscf

    def build_Ax(self, Fmo, Cocc, kappa, Cvirt, Qpq):
        ndocc = np.shape(Cocc)
        Ax = np.dot(Fmo[:ndocc[1], :ndocc[1]], -kappa)
        Ax += np.dot(Fmo[ndocc[1]:, ndocc[1]:], kappa.T).T
        Cright = np.dot(kappa, Cvirt.T).T
        J, K = self.JK.build_DFJK(Qpq, Cocc, Cright)
        Ax += np.dot(Cocc.T, (4*J - K - K.T)).dot(Cvirt)

        return Ax*4


    def SCF_energy(self):
        start = time.time()
        #A = S^(1/2)
        eigval, eigvec = np.linalg.eigh(self.S)
        eigval **= -0.5
        A = np.dot(eigvec*eigval,eigvec.T)
        
        #Ease of use
        nbf = self.nbf
        ndocc = self.ndocc
        nvirt = self.nvirt

        #Initial Diagonalization
        C, Cocc, Cvirt, D = self.diagonalize(self.H,A)
        
        #Size Check
        size = (nbf**4)*8/1.e9
        if size > 14:
            raise Exception("G tensor is too big!")

        #Accessing Qpq through Psi4
        aux = self.psi4.BasisSet.pyconstruct_auxiliary(self.wfn.molecule(), 'DF_BASIS_SCF', '', 'JKFIT', self.psi4.get_global_option('BASIS'))
        zeroC = self.psi4.Matrix(nbf, nbf)
        dfobj = self.psi4.DFTensor(self.wfn.basisset(), aux, zeroC, ndocc, nvirt)
        Qpq = np.asarray(dfobj.Qso())

        #Apply variational method which knows when to stop.
        SCFE = 0
        SCFE_old = 1
        count = 0
        Iter_type = "CORE"
        SOSCF = True

        #Initiate set of trial vectors, error vectors.
        trials = []
        errors = []

        print ("Total time taken for setup: %6.6f" % (time.time() - start))
        itstart = time.time()
        while abs(SCFE_old - SCFE) > self.dE_tol:
            count += 1
            if count > self.maxmacro:
                raise Exception("Calculation Exceeds 100 Iterations!")

            J, K = self.JK.build_DFJK(Qpq, Cocc)
            #Construct Fock Matrix and Compute Energy
            
            F = self.H + 2*J - K
    
            Eelec = np.einsum('qr,qr->',F + self.H, D)
            SCFE_old = SCFE
            SCFE = Eelec + self.Enuc

            r = np.dot(A.T,(np.dot(F, D).dot(self.S)-np.dot(self.S, D).dot(F))).dot(A)
            grad = np.dot(F, D).dot(self.S)-np.dot(self.S, D).dot(F)
            dRMS = np.mean(r**2)**0.5


            #print metrics 
            if count < 10:
                scount = '0'
                scount += str(count)
            else:
                scount = str(count)
            print ('SCF Iteration %s: E = %6.6f  dE = % 2.5E  dRMS = %2.5E , %s' % (scount, SCFE, (SCFE_old - SCFE), dRMS, Iter_type))

            if (SCFE_old - SCFE) < self.dE_tol and dRMS < self.dRMS_tol:
                break

            elif SOSCF and dRMS < 1e-2: #Use SOSCF
                C, Cocc, Cvirt, D, SOSCF = self.SOSCF(C, F, Qpq, self.ndocc, self.nvirt)
                Iter_type = 'SOSCF'
            else: #Use DIIS
                F = self.DIIS(trials, errors, F, r)
                C, Cocc, Cvirt, D = self.diagonalize(F, A)
                Iter_type = 'DIIS'
        
        SCF_time = time.time() - start
        print ("Total time in iterations: %6.3f" % (time.time() - itstart))
        
        print ("Time in microiteratoins: %6.3f" % self.microtime)
        print ("Number of iterations: %d" % count)
        
        
        print ("Macro + Micro iterations: %d\n" % (self.totmicro + count))
        print ("SCF Energy: %12.10f" % SCFE)
        print ("Runtime:      %6.6f\n" % SCF_time)
