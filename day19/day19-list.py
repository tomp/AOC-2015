#!/usr/bin/env python

from collections import defaultdict
import re

infile = "day19-input"

atom_re = re.compile(r"[A-Z][a-z]*")

# All specified gates, indexed by name

def load_input(input):
    rxns = defaultdict(list)
    medicine = ""
    for line in input.splitlines():
        line = line.strip()
        if "=>" in line:
            reactant, product = line.split(' => ')
            rxns[reactant].append(atom_re.findall(product))
        elif len(line) > 0:
            medicine = atom_re.findall(line)
    return rxns, medicine

def replacements(rxns):
    for reactant, products in rxns.items():
        for product in products:
            yield (reactant, product)

def sites(target, reactant):
    """
    Generator that returns all locations of the reactant pattern
    within the target string.
    """
    try:
        pos = target.index(reactant, 0)
        while True:
            yield pos
            pos = target.index(reactant, pos + 1)
    except ValueError:
        pass


if __name__ == '__main__':
    with open(infile, "rb") as fp:
        input = fp.read()

#     input = """
# H => HO
# H => OH
# O => HH
# 
# HOHOHO
# """

    rxns, medicine = load_input(input)

    print "Part 1"

    molecules = set()
    for reactant, product in replacements(rxns):
        print "{} => {}".format(reactant, product)
        rsize = len(reactant)
        for site in sites(medicine, reactant):
            new_molecule = list(medicine)
            new_molecule[site:site+1] = product
            molecules.add("".join(new_molecule))

    print "Found {} product molecules:".format(len(molecules))

    # print
    # print "Part 2"

    
