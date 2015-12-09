#!/usr/bin/env python

import re
from itertools import permutations

infile = "day9-input"

line_re = re.compile(r"(\w+) to (\w+) = (\d+)")

def parse_line(line):
    m = line_re.match(line)
    if m:
        loc1, loc2, dist = m.groups()
        return loc1, loc2, int(dist)
    return None, None, 0

if __name__ == '__main__':
    with open(infile, "rb") as fp:
        input = fp.read()

    print "Part 1"

    nodes = set()
    edges = []
    for line in input.splitlines():
        loc1, loc2, dist = parse_line(line)
        if loc1 is not None:
            print "{} - {} = {}".format(loc1, loc2, dist)
            nodes.add(loc1)
            nodes.add(loc2)
            edges.append((loc1, loc2, dist))

    nodes = sorted(list(nodes))
    print "{} nodes: {}".format(len(nodes), ", ".join(sorted(list(nodes))))

    g = dict([(node, {}) for node in nodes])
    for edge in edges:
        loc1, loc2, dist = edge
        g[loc1][loc2] = dist
        g[loc2][loc1] = dist

    paths = []
    for i, path in enumerate(permutations(nodes)):
        distance = 0
        for loc1, loc2 in zip(path[:-1], path[1:]):
            distance += g[loc1][loc2]

        paths.append((distance, path))
        # print distance, path

    paths.sort()
    print "Shortest path:"
    print paths[0]
    print paths[2]
    print paths[4]
    print

    print "Longest path:"
    print paths[-1]
    print paths[-3]
    print paths[-5]
    


