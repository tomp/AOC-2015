#!/usr/bin/env python

import sys

input_text = "1113222113"

def look_say(input_text):
    output = []
    digits = [int(ch) for ch in input_text]
    last_digit = digits[0]
    count = 1
    for digit in digits[1:]:
        if digit == last_digit:
            count += 1
        else:
            output.extend((count, last_digit))
            last_digit = digit
            count = 1
    output.extend((count, last_digit))
    output_text = "".join([str(digit) for digit in output])
    return output_text

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_text = sys.argv[1]

    print "Part 1"
    print "Input:", input_text

    for i in range(50):
        output_text = look_say(input_text)
        input_text = output_text

    print len(output_text), "characters in final output"
    




