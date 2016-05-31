#author: Mike Zott
import numpy as np
import time

data = open('Euler18Input.dat', 'r')
triangle = [] 
for line in data:
    line_split = line.split()
    line_split = map(int, line_split)
    triangle.append(line_split)

max_path_sum = 0
for row in triangle:
    max_path_sum += max(row)
print max_path_sum

