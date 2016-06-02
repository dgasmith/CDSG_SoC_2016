#author: Mike Zott
import numpy as np

fibol = [1,2]
while fibol[-1] < 4000000:
     fibol.append(fibol[-1]+fibol[-2])
even = np.array(fibol)
even[even %2 != 0] = 0
print even
print sum(even) - even[-1]    

