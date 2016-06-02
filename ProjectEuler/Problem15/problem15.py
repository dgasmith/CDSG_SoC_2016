# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 09:52:11 2016

@author: spolansky
"""

#how the hell am I gonna do this
gridSize = 20
numlist = []

for i in range(1, gridSize + 1):
    paths = ((2 * gridSize) - gridSize + i) / float(i)
    numlist.append(paths)
    print i,
    print paths
    i = i + 1
    
def listsum(numlist):
    theSum = 1
    for i in numlist:
        theSum *= i
    return theSum
    
print (listsum(numlist))