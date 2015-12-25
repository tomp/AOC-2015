#!/usr/bin/env python

import re

infile = "day5-input"

vowel_re = re.compile(r"[aeiou]")
dup_re = re.compile(r"(.)\1")
exclude_re = re.compile(r"(ab|cd|pq|xy)")
repeat_re = re.compile(r"(.).\1")
dup_pair_re = re.compile(r"(..).*\1")

def is_nice(word):
    if exclude_re.search(word):
        return False
    vowel_count = len(vowel_re.findall(word))
    dup = dup_re.search(word)
    return (vowel_count >= 3 and dup is not None)

def is_nice2(word):
    if repeat_re.search(word) is None:
        return False
    return dup_pair_re.search(word) is not None

if __name__ == '__main__':
    with open(infile, "rb") as fp:
        input = fp.read()

    nice_words = []
            
    for word in input.splitlines():
        if len(word) == 0:
            continue
        if is_nice2(word):
            print "GOOD:", word
            nice_words.append(word)
        else:
            print "BAD:", word

    print len(nice_words), "nice words"

