#!/usr/bin/env python

import re

infile = "day23-input"

reg_re = re.compile(r"(hlf|tpl|inc) (a|b)")
jmp_re = re.compile(r"(jmp) ([+-]\d+)")
cond_re = re.compile(r"(jio|jie) (a|b), ([+-]\d+)")

# All specified gates, indexed by name

def load_input(input):
    program = []
    for line in input.splitlines():
        line = line.strip()
        if len(line) == 0:
            continue
        m = reg_re.match(line)
        if m:
            program.append((m.group(1), m.group(2)))
            continue
        m = jmp_re.match(line)
        if m:
            program.append((m.group(1), int(m.group(2))))
            continue
        m = cond_re.match(line)
        if m:
            program.append((m.group(1), m.group(2), int(m.group(3))))
            continue
        raise ValueError("Unable to parse instruction '{}'".format(line))
    return program

def run_program(program, a=0, b=0):
    reg = {'a': a, 'b': b}
    pc = 0
    while pc < len(program) and pc >= 0:
        inst = program[pc]
        print "[{:2d}] a={}, b={} : {}".format(pc, reg['a'], reg['b'], inst)
        if inst[0] == 'inc':
            reg[inst[1]] += 1
            pc += 1
        elif inst[0] == 'tpl':
            reg[inst[1]] *= 3
            pc += 1
        elif inst[0] == 'hlf':
            reg[inst[1]] = reg[inst[1]] // 2
            pc += 1
        elif inst[0] == 'jmp':
            pc += inst[1]
        elif inst[0] == 'jie':
            if reg[inst[1]] % 2 == 0:
                pc += inst[2]
            else:
                pc += 1
        elif inst[0] == 'jio':
            if reg[inst[1]] == 1:
                pc += inst[2]
            else:
                pc += 1
    print "[{:2d}] a={}, b={}".format(pc, reg['a'], reg['b'])
    return (reg['a'], reg['b'])

if __name__ == '__main__':
    with open(infile, "rb") as fp:
        input = fp.read()

    print "Example"
    example = """
inc a
jio a, +2
tpl a
inc a
"""
    program = load_input(example)
    a, b = run_program(program)

    print
    print "Part 1"
    program = load_input(input)
    a, b = run_program(program)
    print "b =", b

    print
    print "Part 2"
    a, b = run_program(program, a=1)
    print "b =", b
