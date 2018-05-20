#!/usr/bin/python

import math
import sys

#
#   ./rmsd.py a.txt b.txt
#
def main() :
    assert len(sys.argv) == 3
    avalues = [float(s) for s in file(sys.argv[1]).readlines()]
    bvalues = [float(s) for s in file(sys.argv[2]).readlines()]
    s = 0.0
    for i in range(len(avalues)) :
        a = avalues[i]
        b = bvalues[i]
        s += (a-b) * (a-b)
    s /= len(avalues)
    s = math.sqrt(s)
    print s

main()


