#!/usr/bin/env python

import sys
import re

infile = "day18-input"

nsteps = 100

class LightArray(object):
    """
    Rectangular light array.

    Light values are stored by rows.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.array = [[0 for row in range(height+2)] for col in range(width+2)]
        self.array[1][1] = 1
        self.array[1][self.width] = 1
        self.array[self.height][self.width] = 1
        self.array[self.height][1] = 1

    def display(self):
        """ Return ascii-art image of the array. """
        lines = []
        for y in range(1, self.height+1):
            line = ["."] * self.width
            for x in range(1, self.width+1):
                if self.array[y][x]:
                    line[x-1] = "#"
            lines.append("".join(line))
        return "\n".join(lines)

    def count_on(self):
        count = 0
        for row in self.array:
            count += row.count(1)
        return count
    
    def advance(self):
        """ Advance array to next step in animtion sequaence """
        count = [[0 for col in range(self.width+2)] for row in range(self.height+2)]
        for y in range(1, self.height+1):
            for x in range(1, self.width+1):
                if self.array[y][x]:
                    count[y][x-1] += 1
                    count[y][x+1] += 1
                    count[y-1][x-1] += 1
                    count[y-1][x] += 1
                    count[y-1][x+1] += 1
                    count[y+1][x-1] += 1
                    count[y+1][x] += 1
                    count[y+1][x+1] += 1
        for y in range(1, self.height+1):
            for x in range(1, self.width+1):
                if count[y][x] == 3:
                    self.array[y][x] = 1
                elif count[y][x] == 2 and self.array[y][x]:
                    self.array[y][x] = 1
                else:
                    self.array[y][x] = 0
        self.array[1][1] = 1
        self.array[1][self.width] = 1
        self.array[self.height][self.width] = 1
        self.array[self.height][1] = 1


def load_input(input):
    lines = [line for line in input.splitlines() if len(line) > 0]
    lights = LightArray(len(lines[0]), len(lines))
    y = 0
    for line in lines:
        if len(line) > 0:
            y += 1
            for pos, ch in enumerate(line):
                x = pos + 1
                if ch == '#':
                    lights.array[y][x] = 1
    return lights

            
if __name__ == '__main__':
    if len(sys.argv) > 1:
        infile = sys.argv[1]

    with open(infile, "rb") as fp:
        input = fp.read()

#     input = """
# .#.#.#
# ...##.
# #....#
# ..#...
# #.#..#
# ####..
# """
#     nsteps = 4
    
    lights = load_input(input)

    print "Part 1"

    print
    print "Initial state"
    print lights.display()

    for i in range(nsteps):
        lights.advance()
        print
        print "Step", i+1
        print lights.display()

    print
    print "After {} steps, {} lights are on".format(nsteps,
            lights.count_on())


