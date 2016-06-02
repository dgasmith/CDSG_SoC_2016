import numpy as np

molecule mol {
H
H 1 0.74
symmetry c1
}

set basis sto-3g

# Build a Psi4 Wavefunction
wfn = psi4.new_wavefunction(mol, 'sto-3g')

# Build a MintsHelper object to supply integrals
mints = psi4.MintsHelper(wfn.basisset())

# Build a overlap matrix
S = mints.ao_overlap()

# Convert Psi4.Matrix to a NumPy array
print np.asarray(S)




