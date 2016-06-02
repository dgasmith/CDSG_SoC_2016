print "Problem 19: Counting Sundays"
import time
start = time.time()
import datetime

import datetime
answer = sum(1 if datetime.date(y, m, 1).weekday() == 6 else 0 for m in xrange(1, 12+1) for y in xrange(1901, 2000+1))

print ("Answer: %d" % answer)
print ("Runtime: %6.6f" % (time.time() - start))
