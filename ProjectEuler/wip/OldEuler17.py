import numpy as np
import time

#one, two, three, four, five, six, seven, eight, nine
ones = [0, 3, 3, 5, 4, 4, 3, 5, 5, 4]

#special tens: ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen,
# seventeen, eighteen, nineteen
specialTens = [3, 6, 6, 8, 8, 7, 7, 9, 9, 8]

#ten, twenty, thirty, fourty, fifty, sixty, seventy, eighty, ninety
tens = [0, 3, 6, 6, 5, 5, 5, 7, 6, 6]

hundred = 7+3
thousand = 8+3

def numToLen(num):
    #print num
    if num == 1000:
        return thousand
    elif num == 100:
        return hundred
    elif num == 1:
        return 3
    temp = 0
    if num / 100 > 0:
        temp += ones[num/100] + hundred + 3
        num = num%100
    if num / 10 > 0:
        if num / 10 == 1:
            temp += specialTens[num%10]
            return temp
        else:
            temp += tens[num/10]
            num = num%10
    if num / 1 > 0:
        
        temp += ones[num]

    return temp

t = time.time()
total = 0
for i in range(1,1001):
    total += numToLen(i)
    

print total
print time.time()-t
            
            
