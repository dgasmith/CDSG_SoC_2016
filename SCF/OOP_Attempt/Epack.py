#SCF Class definitions
import psi4
import time
import numpy as np
import scipy.linalg as sl
from JK_Builder import JK_Builder
from DIIS import DIIS

class Epack:
    
    def __init__(self, wfn, dE_tol, dRMS_tol, maxmacro, DIIS_size, SOSCF_tol, maxmicro):#param for SCF iterations, energy types specified below.
        self.psi4 = psi4
        self.wfn = wfn
        self.dE_tol = dE_tol
        self.maxmacro = maxmacro
        self.dRMS_tol = dRMS_tol
        self.DIIS_size = DIIS_size
        self.SOSCF_tol = SOSCF_tol
        self.maxmicro = maxmicro  #microtime as member data rather than soscf return

        self.Mints = psi4.MintsHelper(self.wfn.basisset())
        self.S = np.asarray(self.Mints.ao_overlap())
        self.T = np.asarray(self.Mints.ao_kinetic())
        self.V = np.asarray(self.Mints.ao_potential())
        self.H = self.T + self.V
        del self.T, self.V, self.Mints
 
        self.DIIS_ = DIIS(self.DIIS_size)
        self.JK = JK_Builder() #JK_Builder probably isn't necceary as a class right now since it has one function and no member data.
        self.Enuc = self.wfn.molecule().nuclear_repulsion_energy()
        self.ndocc = self.wfn.nalpha()
        self.nbf = self.S.shape[0]
        self.nvirt = self.nbf - self.ndocc
        self.microtime = 0.0 #SOSCF iteration data kept as class member data rather than SOSCF() returns
        self.totmicro = 0

    def diagonalize(self, F, A):
        Fp = np.dot(A.T,F).dot(A)
        eigval, eigvec = np.linalg.eigh(Fp)
        C = np.dot(A,eigvec)
        Cocc = C[:,:self.ndocc]
        Cvirt = C[:,self.ndocc:]
        D = np.einsum('pi,qi->pq',Cocc,Cocc)
        return C, Cocc, Cvirt, D
    

    def SOSCF(self, C, F, Qpq, ndocc, nvirt):
        # Remember only the OV part is needed.
        grad = -4 * np.dot(C.T, F).dot(C)[:ndocc, ndocc:]
        Fmo = np.einsum('ij,jk,kl->il', C.T, F, C)              
                   
        eps = np.diag(Fmo)
        precon = -4 * (eps[:ndocc][:, None] - eps[ndocc:])
        k = -grad / precon
        
        Cocc = C[:,:ndocc] 
        Cvirt = C[:,ndocc:]
        Ax = self.build_Ax(Fmo, Cocc, k, Cvirt, Qpq).ravel() #Build DF Hessian
        
        k = k.ravel()
        rk = -grad.ravel() - Ax
        zk = rk / precon.ravel()
        p = zk

        grad_rms = np.mean( grad ** 2) ** 0.5 #Relative metric
        microstart = time.time()

        for j in range(self.maxmicro):

            tmp = self.build_Ax(Fmo, Cocc, p.reshape(ndocc, nvirt), Cvirt, Qpq).ravel()                   

            alpha = np.dot(rk.T, zk)
            alpha /= np.dot(p.T, tmp)
             
            k = k + alpha*p
            rk1 = rk - alpha*tmp
             
            err = np.mean(rk1**2)**0.5
            err = err / grad_rms
            print ("SOSCF Microiteration %d: RMS = %2.5E" % (j+1, err))
            self.totmicro += 1 
            if err < self.SOSCF_tol or j == self.maxmicro - 1:
                
                if j == self.maxmicro - 1:
                    print ("SOSCF could not converge and was turned OFF\n")
                    soscf = False
                else:
                    soscf = True
                break

            zk1 = rk1 / precon.ravel()
            beta = np.dot(zk1.T, rk1) / np.dot(zk.T,rk)
            p = zk1 + beta*p
            
            zk = zk1
            rk = rk1

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


    def energy(self, etype):
        if etype != 'MP2' and etype != 'SCF':
            raise Exception("Unrecognized energy calculation type")
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

        print ("Total time taken for setup: %6.6f" % (time.time() - start))
        itstart = time.time()

        while count < self.maxmacro:
            count += 1
            
            #Construct Fock Matrix and Compute Energy    
            J, K = self.JK.build_DFJK(Qpq, Cocc)
            F = self.H + 2*J - K

            Eelec = np.einsum('qr,qr->', F + self.H, D)
            SCFE_old = SCFE
            SCFE = Eelec + self.Enuc

            grad = np.dot(F, D).dot(self.S) - np.dot(self.S, D).dot(F)
            r = np.dot(A.T, grad).dot(A)
            dRMS = np.mean(r**2)**0.5

            #print metrics 
            if count < 10:
                scount = '0'
                scount += str(count)
            else:
                scount = str(count)
            print ('SCF Iteration %s: E = %6.6f  dE = % 2.5E  dRMS = %2.5E , %s' % (scount, SCFE, (SCFE_old - SCFE), dRMS, Iter_type))

            #Iteration Logic
            if (SCFE_old - SCFE) < self.dE_tol and dRMS < self.dRMS_tol:
                break

            elif SOSCF and dRMS < 1e-2: #Use SOSCF
                C, Cocc, Cvirt, D, SOSCF = self.SOSCF(C, F, Qpq, self.ndocc, self.nvirt)
                Iter_type = 'SOSCF'

            else: #Use DIIS
                F = self.DIIS_.next_trial(F, r)
                C, Cocc, Cvirt, D = self.diagonalize(F, A)
                Iter_type = 'DIIS'
        
        #End of iterations
        if count == self.maxmacro:
            raise Exception("Maximum Number of SCF iterations reached! (%d)" % self.maxmacro)

        SCF_time = time.time() - start
        print ("\nTotal time in iterations: %6.3f" % (time.time() - itstart))
        
        print ("Time in microiteratoins: %6.3f" % self.microtime)
        print ("Number of iterations: %d" % count)
        
        
        print ("Macro + Micro iterations: %d\n" % (self.totmicro + count))
        print ("SCF Energy: %12.10f" % SCFE)
        print ("Runtime:      %6.6f\n" % SCF_time)

        #Calculate MP2 adjustement if specified
        if etype == 'MP2':
            start = time.time()
            C, Cocc, Cvirt, D = self.diagonalize(F,A)

            Qmo = np.einsum('Qpq, pi, qj -> Qij',Qpq, C, C)
            Qmo = Qmo[:, :ndocc, ndocc:]
        
            Fmo = np.einsum('ij,jk,kl->il', C.T, F, C)
            e = np.diag(Fmo)
            ei = e[:ndocc]
            eb = e[ndocc:]

        #Compute (ia I jb)^2 using Qmo
            vv_denom = - eb[:, None] - eb
            tot = 0.0
            for i in range(ndocc):
                for j in range(ndocc):
                    Qa = Qmo[:, i]
                    Qb = Qmo[:, j]
                    ab = np.dot(Qa.T, Qb)

                    numer = ab * (2*ab - ab.T)
                    numer /= (ei[i] + ei[j] + vv_denom)
                    tot += np.sum(numer)

            MP2_time = time.time() - start
  
            print ("MP2 Energy Adjustment: %6.6f" % tot)
            print ("MP2 Energy: %12.10f" % (SCFE + tot))
            print ("MP2 Runtime: %6.6f\n" % (SCF_time + MP2_time))    
