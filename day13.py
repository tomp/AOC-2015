#!/usr/bin/env python

import sys
import re
from collections import defaultdict
from itertools import permutations

infile = "day13-input"

line_re = re.compile(r"^(\w+) .* (lose|gain) (\d+) .* to (\w+)")

def rate_seating(seating):
    total = 0
    total += happiness[seating[0]][seating[-1]]
    total += happiness[seating[-1]][seating[0]]
    for i in range(1, len(seating)):
        total += happiness[seating[i-1]][seating[i]]
        total += happiness[seating[i]][seating[i-1]]
    return total

if __name__ == '__main__':
    if len(sys.argv) > 1:
        infile = sys.argv[1]

    with open(infile, "rb") as fp:
        input = fp.read()
    
    happiness = defaultdict(dict)
    for line in input.splitlines():
        m = line_re.match(line)
        if m is not None:
            guest1, gainlose, units, guest2 = m.groups()
            if gainlose == 'gain':
                units = int(units)
            else:
                units = -int(units)
            happiness[guest1][guest2] = units

    guests = sorted(happiness.keys())
    print len(guests), "guests:"
    print ", ".join(guests)

    print "Part 1"
    scores = []
    for seating in permutations(guests[1:]):
        complete_seating = [guests[0]] + list(seating)
        score = rate_seating(complete_seating)
        print "Score: {:3d}  Seating: {}".format(score, complete_seating)
        scores.append((score, complete_seating))

    scores.sort(reverse=True)
    print
    for score, seating in scores[:5]:
        print "Score: {:3d}  Seating: {}".format(score, seating)

    print "Part 2"
    for guest in guests:
        happiness[guest]["me"] = 0
        happiness["me"][guest] = 0
    guests.append("me")

    scores = []
    for seating in permutations(guests[1:]):
        complete_seating = [guests[0]] + list(seating)
        score = rate_seating(complete_seating)
        print "Score: {:3d}  Seating: {}".format(score, complete_seating)
        scores.append((score, complete_seating))

    scores.sort(reverse=True)
    print
    for score, seating in scores[:5]:
        print "Score: {:3d}  Seating: {}".format(score, seating)


    




    

