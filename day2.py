#!/usr/bin/env python

infile = "day2-input"

with open(infile, "rb") as fp:
    input = fp.read()

total_paper = 0
total_ribbon = 0

for num, box in enumerate(input.splitlines()):
    if 'x' in box:
        length, width, height = [int(item) for item in box.split('x')]
        areas = [length * width, width * height, length * height]
        perimeters = [2*(length + width), 2*(width + height),
                2*(length + height)]
        volume = length * width * height
        areas.sort()
        perimeters.sort()
        paper = (3 * areas[0]) + (2 * areas[1]) + (2 * areas[2])
        ribbon = perimeters[0] + volume
        print "box {}: {:3d} sq ft paper, {:2d} ft ribbon ({} x {} x {})".format(
                num+1, paper, ribbon, length, width, height)
        total_paper += paper
        total_ribbon += ribbon
print "Total paper area:", total_paper
print "Total ribbon length:", total_ribbon
