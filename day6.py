#!/usr/bin/env python

import re

infile = "day6-input"

class LightArray(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.array = [[False for row in range(height)] for col in range(width)]

    def display(self):
        """ Return ascii-art image of the array. """
        lines = []
        for row in range(self.height):
            y = self.height - row - 1
            line = ["."] * self.width
            for x in range(self.width):
                if self.array[x][y]:
                    line[x] = "@"
            lines.append("".join(line))
        return "\n".join(lines)

    def count_on(self):
        count = 0
        for column in self.array:
            count += column.count(True)
        return count

    def set_region(self, start, end, value):
        for y in range(start[1], end[1]+1):
            for x in range(start[0], end[0]+1):
                self.array[x][y] = value

    def toggle_region(self, start, end):
        for y in range(start[1], end[1]+1):
            for x in range(start[0], end[0]+1):
                self.array[x][y] = not self.array[x][y]

class DimmableLightArray(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.array = [[0 for row in range(height)] for col in range(width)]

    def display(self):
        """ Return ascii-art image of the array. """
        lines = []
        for row in range(self.height):
            y = self.height - row - 1
            lines.append("".join([str(self.array[x][y]) for x in
                range(self.width)]))
        return "\n".join(lines)

    def total_brightness(self):
        total = 0
        for column in self.array:
            for brightness in column:
                total += brightness
        return total

    def set_region(self, start, end, value):
        for y in range(start[1], end[1]+1):
            for x in range(start[0], end[0]+1):
                self.array[x][y] = value

    def increment_region(self, start, end, incr):
        for y in range(start[1], end[1]+1):
            for x in range(start[0], end[0]+1):
                self.array[x][y] += incr
                if self.array[x][y] < 0:
                    self.array[x][y] = 0

line_re = re.compile(r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)")

if __name__ == '__main__':
    with open(infile, "rb") as fp:
        input = fp.read()

    print "Part 1"
    lights = LightArray(1000, 1000)

    for line in input.splitlines():
        m = line_re.match(line)
        if m is None:
            print "skipped line '{}'".format(line)
            continue
        op, x0, y0, x1, y1 = m.groups()
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        if op == "turn on":
            lights.set_region((x0, y0), (x1, y1), True)
        elif op == "turn off":
            lights.set_region((x0, y0), (x1, y1), False)
        elif op == "toggle":
            lights.toggle_region((x0, y0), (x1, y1))

    print lights.count_on(), "lights lit"
    print

    print "Part 2"
    lights = DimmableLightArray(1000, 1000)

    for line in input.splitlines():
        m = line_re.match(line)
        if m is None:
            print "skipped line '{}'".format(line)
            continue
        op, x0, y0, x1, y1 = m.groups()
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        if op == "turn on":
            lights.increment_region((x0, y0), (x1, y1), 1)
        elif op == "turn off":
            lights.increment_region((x0, y0), (x1, y1), -1)
        elif op == "toggle":
            lights.increment_region((x0, y0), (x1, y1), 2)

    print "Total brightness:", lights.total_brightness()

