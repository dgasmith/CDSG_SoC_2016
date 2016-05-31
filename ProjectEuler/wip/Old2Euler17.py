import numpy as np
import time

t = time.time()

#one, two, three, four, five, six, seven, eight, nine
ones = [0, 3, 3, 5, 4, 4, 3, 5, 5, 4]

#special tens: ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen,
# seventeen, eighteen, nineteen
specialTens = [3, 6, 6, 8, 8, 7, 7, 9, 8, 8]

#ten, twenty, thirty, forty, fifty, sixty, seventy, eighty, ninety
tens = [0, 3, 6, 6, 5, 5, 5, 7, 6, 6]

hundred = 7
thousand = 8

def numToLen(num):
    print num    
    if num == 100:
        return hundred + 3
    temp = 0
    num = str(num)
    if len (num) == 4:
        return 3 + thousand
    if len(num) == 3:
        if num[1] != '1':
            return ones[int(num[0])] + hundred + 3 + tens[int(num[1])] + ones[int(num[2])]
        else:
            print "hey3"
            return ones[int(num[0])] + hundred + 3 + specialTens[int(num[2])]
    if len(num) == 2:
        if num[0] != '1':
            return tens[int(num[0])] + ones[int(num[1])]
        else:
            print "hey2"
            return specialTens[int(num[1])]
    if len(num) == 1:
        return ones[int(num[0])]
    return temp

total = 0
for i in range(1,30):
    total += numToLen(i)
    print numToLen(i)

print total
print time.time()-t
            
            
