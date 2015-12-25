#!/usr/bin/env python

import sys
import re

from collections import defaultdict

infile = "day14-input"
race_duration = 2503

line_re = re.compile(r"^(\w+) can fly (\d+) km.s for (\d+) seconds,.* for (\d+) seconds")

speed = {}
duration = {}
rest = {}

def load_input(input):
    global speed, duration, rest
    for line in input.splitlines():
        m = line_re.match(line)
        if m:
            name = m.group(1)
            speed[name] = int(m.group(2))
            duration[name] = int(m.group(3))
            rest[name] = int(m.group(4))
        elif len(line) > 0:
            raise Exception("Unable to parse line '{}'".format(line))

def positions(elapsed_time):
    # print
    # print "Elapsed time:", elapsed_time
    results = []
    for name in sorted(speed.keys()):
        period = duration[name] + rest[name]
        periods = elapsed_time // period
        remaining = elapsed_time % period
        dist_per_period = speed[name] * duration[name]
        distance = periods * dist_per_period
        if remaining < duration[name]:
            distance += speed[name] * remaining
        else:
            distance += dist_per_period
        results.append((distance, name))
        # print "{:10s}:  distance: {} km,  periods: {}, km/period: {}, remaining: {} sec".format(
        #         name, distance, periods, dist_per_period, remaining)
    return sorted(results, reverse=True)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        infile = sys.argv[1]

    with open(infile, "rb") as fp:
        input = fp.read()
    
    load_input(input)

    print "Part 1"
    final = positions(race_duration)
    print
    print "Elapsed time:",race_duration
    for distance, name in final:
        print distance, name

    print
    print "Part 2"
    points = defaultdict(int)
    for elapsed_time in range(1, race_duration+1):
        field = positions(elapsed_time)
        print
        print "Time:", elapsed_time
        lead_position = field[0][0]
        for distance, name in field:
            if distance == lead_position:
                points[name] += 1
            print distance, name, points[name]


