#!/usr/bin/python

import sys
import time

for i in range(0,100) :
    sys.stdout.write('\rHello, %d\n' % i)
    sys.stdout.flush()
    time.sleep(0.1)



