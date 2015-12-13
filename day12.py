#!/usr/bin/env python

import sys
import re
import json

infile = "day12-input"

number_re = re.compile(r"(?<![\"\d-])-?\d+(?![\"\d])")

def extract_numbers(text):
    return [int(x) for x in number_re.findall(text)]

def remove_red_objects(input_obj):
    if isinstance(input_obj, dict):
        return remove_red_objects_from_dict(input_obj)
    elif isinstance(input_obj, list):
        return remove_red_objects_from_list(input_obj)
    else:
        return input_obj

def remove_red_objects_from_dict(input_dict):
    assert isinstance(input_dict, dict)
    output_dict = {}
    if "red" not in input_dict.values():
        for k, v in input_dict.iteritems():
            output_dict[k] = remove_red_objects(v)
    return output_dict

def remove_red_objects_from_list(input_list):
    assert isinstance(input_list, list)
    output_list = []
    for v in input_list:
        output_list.append(remove_red_objects(v))
    return output_list

if __name__ == '__main__':
    if len(sys.argv) > 1:
        infile = sys.argv[1]

    with open(infile, "rb") as fp:
        input = fp.read()

    print "Part 1"
    numbers = extract_numbers(input)
    total = sum(numbers)
    print "Found {} numbers in the input".format(len(numbers))
    print "Sum is", total
    

    print "Part 2"
    input_obj = json.loads(input)
    stripped_obj = remove_red_objects(input_obj)
    stripped_text = json.dumps(stripped_obj)
    numbers = extract_numbers(stripped_text)
    total = sum(numbers)
    print "Found {} numbers in the stripped input".format(len(numbers))
    print "Sum is", total



