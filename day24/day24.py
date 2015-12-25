#!/usr/bin/env python

import sys
import re
from operator import __mul__
from collections import defaultdict
from itertools import combinations

infile = "day24-input"

line_re = re.compile(r"\d+$")

def load_input(input):
    weights = []
    for line in input.splitlines():
        if len(line) > 0:
            weights.append(int(line))
    return weights

def product(numbers):
    return reduce(__mul__, numbers, 1)

def remove_from_list(input_list, remove_list):
    result = list(input_list)
    for item in remove_list:
        i = result.index(item)
        result[i:i+1] = []
    return result

if __name__ == '__main__':
    if len(sys.argv) > 1:
        infile = sys.argv[1]

    with open(infile, "rb") as fp:
        input = fp.read()

    weights = load_input(input)
    total_weight = sum(weights)
    assert total_weight % 3 == 0

    print "{} packages, total weight is {}".format(len(weights), total_weight)

    weights.sort(reverse=True)

    print
    print "Part 1"

    ngroups = 3
    group_weight = total_weight // ngroups
    print "Split packages into {} groups, each weighing {}".format(
            ngroups, group_weight)
    results = []
    min_qe = None

    for size1 in range(5, len(weights) // 3):
        for group1_weights in combinations(weights, size1):
            if sum(group1_weights) == group_weight:
                qe = product(group1_weights)
                if min_qe is None or qe <= min_qe:
                    print "Size: {}  QE: {}  group1: {}".format(size1, qe, ", ".join([
                        str(w) for w in group1_weights]))
                    weights2 = remove_from_list(weights, group1_weights)
                    for size2 in range(5, (len(weights2) - 5)):
                        for group2_weights in combinations(weights2, size2):
                            if sum(group2_weights) == group_weight:
                                results.append((size1, qe, group1_weights, group2_weights))
                                if min_qe is None or qe < min_qe:
                                    min_qe = qe

        if results:
            break

    results.sort()

    print
    for size1, qe, group1_weights, group2_weights in results[:5]:
        print "Size: {}  QE: {}  group1: {}  group2: {}".format(size1, qe, ", ".join([
            str(w) for w in group1_weights]), ", ".join([str(w) for w in group2_weights]))

    print
    print "Part 2"

    ngroups = 4
    group_weight = total_weight // ngroups
    print "Split packages into {} groups, each weighing {}".format(
            ngroups, group_weight)
    results = []
    min_qe = None

    for size1 in range(4, len(weights)):
        for group1_weights in combinations(weights, size1):
            if sum(group1_weights) == group_weight:
                qe = product(group1_weights)
                if min_qe is None or qe <= min_qe:
                    print "Size: {}  QE: {}  group1: {}".format(size1, qe, ", ".join([
                        str(w) for w in group1_weights]))
                    weights2 = remove_from_list(weights, group1_weights)
                    for size2 in range(5, (len(weights2) - 4)):
                        for group2_weights in combinations(weights2, size2):
                            if sum(group2_weights) == group_weight:
                                weights3 = remove_from_list(weights2, group2_weights)
                                for size3 in range(5, (len(weights3) - 4)):
                                    for group3_weights in combinations(weights3, size3):
                                        if sum(group3_weights) == group_weight:
                                            # print "-------- group2: {}  group3: {}".format(
                                            #         ", ".join([str(w) for w in group2_weights]),
                                            #         ", ".join([str(w) for w in group3_weights]))
                                            results.append((size1, qe, group1_weights, group2_weights, group3_weights))
                                            if min_qe is None or qe < min_qe:
                                                min_qe = qe
        if results:
            break

    results.sort()

    print
    for size1, qe, group1_weights, group2_weights, group3_weights in results[:5]:
        print "Size: {}  QE: {}  group1: {}  group2: {}  group3: {}".format(size1, qe,
                ", ".join([str(w) for w in group1_weights]),
                ", ".join([str(w) for w in group2_weights]),
                ", ".join([str(w) for w in group3_weights]))

