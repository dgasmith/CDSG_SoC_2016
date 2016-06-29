#DIIS class definitions
import numpy as np

class DIIS:

    def __init__(self, kept_trials):
        self.trials = []
        self.errors = []
        self.kept_trials = kept_trials    

    def next_trial(self, F, r):

        self.trials.append(F)

        #Obtain DIIS error    
        if len(self.errors) > self.kept_trials: #only keep the 8th most recent guesses for use.
            del self.errors[0]
            del self.trials[0]
        self.errors.append(r)

        #Build B
        size = len(self.errors) + 1
        B = np.zeros((size, size))
        B[-1] = -1
        B[:,-1] = -1
        B[-1,-1] = 0
        for i in range(size-1):
            for j in range(size-1):
                B[i,j] = np.sum(self.errors[i] * self.errors[j])

        #Solve for Cn
        vec = np.zeros(size)
        vec[-1] = -1
        inverse = np.linalg.inv(B)
        Cn = np.linalg.solve(B, vec)

        #Rebuild Fock Matrix according to Cn
        F = np.zeros_like(F)
        for i in range(len(Cn) - 1):
            F += Cn[i] * self.trials[i]

        return F
        #Diagonalize F and Reproduce Density Matrix after!!

