#!/usr/bin/python

import random
import sys

def main() :
    assert len(sys.argv) >= 2
    for i in range(1,len(sys.argv)) :
        f = file(sys.argv[i], "r")
        lines = []
        for line in f.readlines() :
            lines.append(line)
        f.close()
        random.shuffle(lines)
        f = file(sys.argv[i], "w")
        f.write("".join(lines))
        f.close()

main()
    

