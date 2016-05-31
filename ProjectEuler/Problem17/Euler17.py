import numpy as np
import time

t = time.time()

#one, two, three, four, five, six, seven, eight, nine
ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

#special tens: ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen,
# seventeen, eighteen, nineteen
specialTens = ['ten', 'eleven', 'twleve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']

#ten, twenty, thirty, forty, fifty, sixty, seventy, eighty, ninety
tens = ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']


def numToWord(num):
    word = ''
    num = str(num)
    if len(num) == 4:
        return 'onethousand'
    if len(num) == 3:
        word += ones[int(num[0])] + 'hundred' 
        if num[1] != '0' or num[2] != '0':
            word += 'and'
        if num[1] != '1':
            word += tens[int(num[1])] + ones[int(num[2])]
        else:
            word += specialTens[int(num[2])]
    if len(num) == 2:
        if num[0] != '1':
            word += tens[int(num[0])] + ones[int(num[1])]
        else:
            word += specialTens[int(num[1])]
    if len(num) == 1:
        word += ones[int(num[0])]
    return word
total = 0
for i in range(1,1001):
    print numToWord(i)
    total += len(numToWord(i))


print total
print time.time()-t
            
            
