#!/usr/bin/env python

from collections import defaultdict
from copy import deepcopy
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
            rxns[reactant].append(product)
        elif len(line) > 0:
            medicine = line
    return rxns, medicine

def reverse_reactions(rxns):
    """
    Return a table of reverse reactions for the given reactions.
    """
    rev_rxns = defaultdict(list)
    for reactant, products in rxns.items():
        for product in products:
            rev_rxns[product].append(reactant)
    return rev_rxns

def next_reaction(rxns):
    reactants = sorted(rxns.keys(), reverse=True)
    for reactant in reactants:
        for product in rxns[reactant]:
            yield (reactant, product)

def sites(target, reactant):
    """
    Generator that returns all locations of the reactant pattern
    within the target string.
    """
    pos = target.find(reactant, 0)
    while pos > -1:
        yield pos
        pos = target.find(reactant, pos+1)

def apply_reaction(precursor, site, reactant, product):
    rsize = len(reactant)
    return precursor[:site] + product + precursor[(site + rsize):]

synthesis = {}

def reverse_synthesis(target, rev_rxns):
    """
    Return all synthetic routes that lead from 'e' to the given target.

    A route is a list of (site, reactant, product) tuples.
    """
    global depth, count
    if target in synthesis:
        # print "[{}]".format(target)
        return synthesis[target]

    # print "reverse_synthesis('{}')".format(target)
    routes = []
    for reactant, product in next_reaction(rev_rxns):
        if product == 'e' and len(target) > len(reactant):
            continue
        if not reactant in target:
            continue
        for site in sites(target, reactant):
            step = (site, reactant, product)
            precursor = apply_reaction(target, *step)
            # print "{} --> {}".format(step, precursor)
            if precursor == "e":
                routes.append([step])
                # print "...", len(routes), "routes:", routes
                count += 1
                print "**** solution {} at depth {}".format(count, depth)
            elif not "e" in precursor:
                # print "..."
                depth += 1
                preroutes = reverse_synthesis(precursor, rev_rxns)
                if preroutes:
                    preroutes = deepcopy(preroutes)
                    # print "...", len(preroutes), "preroutes:", preroutes
                    for route in preroutes:
                        route.append(step)
                    routes.extend(preroutes)
                    # print "...", len(routes), "routes:", routes
                depth -= 1
    # print "<--", routes
    synthesis[target] = routes
    return routes

if __name__ == '__main__':
    with open(infile, "rb") as fp:
        input = fp.read()

#     input = """
# e => H
# e => O
# H => HO
# H => OH
# O => HH
# 
# HOHOHO
# """

    rxns, medicine = load_input(input)
    for reactant, product in next_reaction(rxns):
        print "{} => {}".format(reactant, product)

    print
    print "Part 1"

    molecules = set()
    for reactant, product in next_reaction(rxns):
        for site in sites(medicine, reactant):
            molecules.add(apply_reaction(medicine, site, reactant, product))

    print "Found {} product molecules:".format(len(molecules))

    print
    print "Part 2"

    rev_rxns = reverse_reactions(rxns)

    depth = 0
    count = 0
    all_routes = reverse_synthesis(medicine, rev_rxns)
    print "Found {} routes to {}".format(len(all_routes), medicine)

    all_routes = [(len(route), route) for route in all_routes]
    all_routes.sort(reverse=True)

    for i, item in enumerate(all_routes):
        nsteps, route = item
        print
        print "[{}] {} steps".format(i+1, nsteps)
        molecule = 'e'
        for site, product, reactant in route:
            molecule = apply_reaction(molecule, site, reactant, product)
            print "@{}  {} => {}  {}".format(site, reactant, product, molecule)



