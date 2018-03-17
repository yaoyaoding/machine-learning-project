#!/usr/bin/python

import random

# start
row = 1000
col = 1000

for i in range(row) :
    x = [random.randint(0,1) for j in range(col)]
    y = sum(x) % 2
    print y,
    for j in range(col) :
        print "%d:%d " % (j, x[j]),
    print



