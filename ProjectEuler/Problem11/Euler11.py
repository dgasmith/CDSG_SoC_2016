import numpy as np
import time

grid = np.loadtxt('Euler11Input.dat', dtype = int)
t = time.time()
product = 0

for i in range(len(grid[0])-3):
    for j in range(len(grid[0])): #square grid
        if np.product(grid[j][i:4+i]) > product:
            product = np.product(grid[j][i:4+i]) #product of four numbers horizontally
        if np.product(grid[i:4+i, j]) > product:
            product = np.product(grid[i:4+i, j]) #product of four numbers vertically

for i in range(-len(grid[0])+3 , len(grid[0])-3 ):
    for j in range(len(np.diagonal(grid, i))-3):
        if np.product(np.diagonal(grid, i)[j:j+4]) > product:
            product = np.product(np.diagonal(grid, i)[j:j+4])         
        if np.product(np.diagonal(np.fliplr(grid), i)[j:j+4]) > product:
            product = np.product(np.diagonal(np.fliplr(grid), i)[j:j+4])


print grid        
print grid.T
print product
print time.time()-t
