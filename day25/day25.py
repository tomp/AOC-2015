#!/usr/bin/env python

code1 = 20151125
mult = 252533
modulus = 33554393

def code_number(row, col):
    code_level = row + (col -1)
    return col + (code_level * (code_level - 1) // 2)

def code(row, col):
    code = code1
    count = code_number(row, col)
    for i in range(count-1):
        code = (code * mult) % modulus
    return code

if __name__ == '__main__':
    row, col = 3010, 3019
