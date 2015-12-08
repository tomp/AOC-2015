#!/usr/bin/env python

import re

infile = "day7-input"

# All specified gates, indexed by name
gates = {}

# All gates that have output values.
gates_done = []

# indentation depth for debug output
depth = 0

wire_re = re.compile(r"^[a-z]+$")

def is_wire(name):
    return (wire_re.match(name) is not None)

class Gate(object):
    """
    A logic gate, specified by
    - an operation (SET, AND, OR, NOT, LSHIFT<n>, or RSHIFT<n>)
    - 0, 1 or 2 inputs (wire names, or values)
    - an output wire name

    Each instantiated gate has a unique output wire name, which
    can be used to identify the gate.
    """
    def __init__(self, name, op, input1=None, input2=None):
        if input1 is not None and input2 is not None:
            self.description = " ".join((input1, op, input2))
        elif input1 is None:
            self.description = " ".join((op, input2))
        else:
            self.description = input1
        # print "#DEF", name, '<-', self.description
        self.name = name
        self.op = op
        self.input1 = input1
        self.input2 = input2
        self.value1 = None
        self.result = None
        if self.op == "SET":
            assert input1 is not None
            assert input2 is None
            if not is_wire(input1):
                self.value1 = int(input1)
                gates_done.append(self)
        elif self.op == "LSHIFT" or self.op == "RSHIFT":
            assert is_wire(input1)
            self.bits = int(input2)
        elif self.op == "NOT":
            assert input1 is None
            assert input2 is not None
            assert is_wire(input2)
        elif self.op == "AND":
            assert input1 is not None
            assert input2 is not None
            assert is_wire(input2)
            if not is_wire(input1):
                self.value1 = int(input1)
        elif self.op == "OR":
            assert input1 is not None
            assert input2 is not None
            assert is_wire(input2)
            if not is_wire(input1):
                self.value1 = int(input1)

    def value(self):
        global depth
        # print "EVAL", self.name, '<-', self.description
        if self.result is None:
            depth += 1
            if self.op == "SET":
                if self.value1 is not None:
                    self.result = self.value1
                else:
                    self.result = gates[self.input1].value()
            elif self.op == "NOT":
                self.result = ~gates[self.input2].value()
            elif self.op == "RSHIFT":
                self.result = (gates[self.input1].value() >> self.bits)
            elif self.op == "LSHIFT":
                self.result = (gates[self.input1].value() << self.bits)
            elif self.op == "AND":
                if self.value1 is not None:
                    self.result = (self.value1 & gates[self.input2].value())
                else:
                    self.result = (gates[self.input1].value() &
                            gates[self.input2].value())
            elif self.op == "OR":
                if self.value1 is not None:
                    self.result = (self.value1 | gates[self.input2].value())
                else:
                    self.result = (gates[self.input1].value() |
                            gates[self.input2].value())
            depth -= 1
            # print "{}{} = {} <- {}".format("   " * depth, self.name,
            #         self.result, self.description)
        return self.result

set_re = re.compile(r"[0-9]+$")
not_re = re.compile(r"[0-9]+$")

def parse_line(line):
    try:
        inputs, name = line.split(' -> ')
        words = inputs.split()
        if len(words) == 1:
            return name, 'SET', words[0], None
        elif len(words) == 2:
            return name, words[0], None, words[1]
        elif len(words) == 3:
            return name, words[1], words[0], words[2]
        return None, None, None, None
    except:
        return None, None, None, None

if __name__ == '__main__':
    with open(infile, "rb") as fp:
        input = fp.read()

    print "Part 1"

    for line in input.splitlines():
        name, op, input1, input2 = parse_line(line)
        if op is not None:
            gates[name] = Gate(name, op, input1, input2)
    
    a_value = gates["a"].value()
    print "value of 'a' is", a_value

    for gate in gates.values():
        gate.result = None

    print "Part2"
    print "Reset wire 'b' to", a_value

    gates["b"] = Gate("b", "SET", str(a_value), None)

    print "value of 'a' is", gates["a"].value()
    print

