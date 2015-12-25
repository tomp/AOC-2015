#!/usr/bin/env python

import re

infile = "day8-input"

hex_re = re.compile(r"\\x[0-9a-f][0-9a-f]")
quote_re = re.compile(r"\\\"")
slash_re = re.compile(r"\\\\")

if __name__ == '__main__':
    with open(infile, "rb") as fp:
        input = fp.read()

    code_chars = 0
    input_chars = 0
    string_chars = 0
    eval_chars = 0
    for line in input.splitlines():
        if len(line) == 0:
            continue
        orig_line = line

        input_chars += len(orig_line)

        parsed_line = eval(orig_line)
        eval_chars += len(parsed_line)

        line = orig_line.strip('"')
        line = " {} ".format(line)
        line = slash_re.sub(r"_", line)
        line = quote_re.sub('"', line)
        line = hex_re.sub("?", line)
        line = line.replace("_", '"')
        line = line.strip(" ")
        string_chars += len(line)

        encoded_line = orig_line.replace('\\', '\\\\')
        encoded_line = encoded_line.replace('"', '\\\"')
        encoded_line = '"' + encoded_line + '"'
        code_chars += len(encoded_line)

        try:
            check_line = eval(encoded_line)
        except:
            check_line = ""

        if len(parsed_line) != len(line):
            print "Line: '{}'".format(orig_line)
            print "Eval: '{}'".format(parsed_line)
            print "Mine: '{}'".format(line)
            print

        if len(orig_line) != len(check_line):
            print "Line: '{}'".format(orig_line)
            print "Code: '{}'".format(encoded_line)
            print "Eval: '{}'".format(check_line)
            print

    print "Characters in input:", input_chars
    print "Characters of data:", string_chars
    print "Characters of data:", eval_chars
    print "Extra code characters:", input_chars - string_chars
    print

    print "Encoded input characters:", code_chars
    print "Extra characters for encoding:", code_chars - input_chars

