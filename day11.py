#!/usr/bin/env python

import sys
import re

input_password = "vzbxkghb"

doubles_re = re.compile(r"([a-z])\1.*([a-z])\2")
forbidden_re = re.compile(r"[ilo]")

charset_size = 26
maxchar = charset_size - 1
charset = [chr(ord('a')+i) for i in range(charset_size)]

def increment_password(password):
    chars = [ord(ch)-ord('a') for ch in password]
    pos = len(chars) - 1
    chars[pos] += 1
    while chars[pos] > maxchar and pos > 0:
        chars[pos] = 0
        pos -= 1
        chars[pos] += 1
    if chars[pos] > maxchar and pos == 0:
        chars[pos] = 0
    new_password = "".join([chr(ord('a')+ch) for ch in chars])
    return new_password

def is_valid(password):
    if len(password) != 8:
        return False
    if forbidden_re.search(password):
        return False
    if not doubles_re.search(password):
        return False
    if not has_straight(password):
        return False
    return True

def has_straight(password):
    chars = [ord(ch)-ord('a') for ch in password]
    for i in range(len(chars)-2):
        if chars[i+1] == chars[i]+1 and chars[i+2] == chars[i+1]+1:
            return True
    return False

def next_password(password):
    password = increment_password(password)
    while not is_valid(password):
        password = increment_password(password)
    return password
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_password = sys.argv[1]

    print "Part 1"
    print "Input password:", input_password

    print "Next password:", password
    




