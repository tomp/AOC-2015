#!/usr/bin/env python

import sys

if len(sys.argv) > 1:
    infile = sys.argv[1]
else:
    infile = "day3-input"

with open(infile, "rb") as fp:
    input = fp.read()

x = 0
y = 0
x2 = 0
y2 = 0
presents = {}
present_count = 1

presents[(x,y)] = presents.get((x,y), 0) + 1
presents[(x2,y2)] = presents.get((x2,y2), 0) + 1

turn = 0
for move in input:
    if turn == 0:
        if move == '^':
            y += 1
        elif move == 'v':
            y -= 1
        elif move == '>':
            x += 1
        elif move =='<':
            x -= 1
        else:
            continue
        presents[(x,y)] = presents.get((x,y), 0) + 1
        turn = 1
    elif turn == 1:
        if move == '^':
            y2 += 1
        elif move == 'v':
            y2 -= 1
        elif move == '>':
            x2 += 1
        elif move =='<':
            x2 -= 1
        else:
            continue
        presents[(x2,y2)] = presents.get((x2,y2), 0) + 1
        turn = 0
    present_count += 1

print present_count, "presents were given."
print len(presents), "houses received at least one present."


