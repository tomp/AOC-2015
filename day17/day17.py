#!/usr/bin/env python

import sys
import re
import math

infile = "day17-input"

total_volume = 150

def load_input(input):
    volumes = []
    for line in input.splitlines():
        if len(line) > 0:
            volumes.append(int(line))
    return sorted(volumes, reverse=True)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        infile = sys.argv[1]

    with open(infile, "rb") as fp:
        input = fp.read()
    
    volumes = load_input(input)

    # volumes = [13,8, 5, 3, 2, 1, 1]
    # total_volume = 15

    print len(volumes), "containers available"
    print ", ".join([str(v) for v in volumes])

    # print "Part 1"

    stack = [(0, volumes[0])]
    results = []
    while True:
        print "    ", stack
        idx, volume = stack[-1]
        next_idx = idx + 1
        try:
            if volume < total_volume:
                # need more containers...
                if next_idx < len(volumes):
                    # add the next smallest container
                    stack.append((next_idx, volume + volumes[next_idx]))
                else:
                    # no more smaller containers to add
                    # remove last container
                    stack.pop()
                    # try to replace second smallest container with next smallest
                    idx, volume = stack.pop()
                    new_idx = idx + 1
                    new_volume = volume - volumes[idx] + volumes[new_idx]
                    stack.append((new_idx, new_volume))
            elif volume >= total_volume:
                # drop last container and try next smallest
                if volume == total_volume:
                    results.append((len(stack)+1, [item[0] for item in stack]))
                    print "****", stack
                idx, volume = stack.pop()
                new_idx = idx + 1
                if new_idx == len(volumes):
                    idx, volume = stack.pop()
                    new_idx = idx + 1
                new_volume = volume - volumes[idx] + volumes[new_idx]
                stack.append((new_idx, new_volume))
        except IndexError:
            break


    results.sort(reverse=True)
    for i, solution in enumerate(results):
        print "{:2d}: ({}) {}".format(i+1, solution[0], ", ".join([str(volumes[k]) for k in solution[1]]))
    
