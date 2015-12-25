#!/usr/bin/env python

import math
import numpy as np

if __name__ == '__main__':

    min_presents = 34000000
    min_units = min_presents/10

    print "Part 1"

    # min_presents = 1000
    # min_units = min_presents // 10
    max_num = min_units // 4
    print "Find first house with at least {} presents".format(min_presents)
    print "Consider up to {} houses".format(max_num)

    total = np.zeros(max_num+1, dtype=int)
    
    for i in range(1, max_num+1):
        n = max_num // i
        idx = i * np.array(range(1, n+1))
        total[idx] += i*10

    for i in range(1, max_num+1):
        if total[i] >= min_presents:
            print "House {} got {} presents".format(i, total[i])
            break

    print
    print "Part 2"

    # min_presents = 1000
    # min_units = min_presents // 10
    max_num = min_units // 4
    print "Find first house with at least {} presents".format(min_presents)
    print "Consider up to {} houses".format(max_num)

    total = np.zeros(max_num+1, dtype=int)
    
    for i in range(1, max_num+1):
        n = max_num // i
        if n > 50:
            n = 50
        idx = i * np.array(range(1, n+1))
        total[idx] += i*11

    for i in range(1, max_num+1):
        if total[i] >= min_presents:
            print "House {} got {} presents".format(i, total[i])
            break
        
    
    


