#!/usr/bin/env python

import sys
import re

from collections import defaultdict, namedtuple

infile = "day15-input"
total_amount = 100

line_re = re.compile(r"^(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)")

Ingredient = namedtuple('Ingredient', ['capacity', 'durability', 'flavor', 'texture', 'calories'])

def load_input(input):
    ingredients = {}
    for line in input.splitlines():
        m = line_re.match(line)
        if m:
            name = m.group(1)
            ingredient = Ingredient._make([int(item) for item in m.groups()[1:]])
            ingredients[name] = ingredient
        elif len(line) > 0:
            raise Exception("Unable to parse line '{}'".format(line))
    return ingredients

def score_recipe(recipe, ingredients, verbose=False):
    components = [0, 0, 0, 0, 0]
    for name, amount in recipe:
        for i, value in enumerate(ingredients[name]):
            components[i] += amount * value
        if verbose:
            print "             ", "   ".join([str(amount*value) for value in ingredients[name]])
    if verbose:
        print "score = prod(", " * ".join([str(x) for x in components[:-1]]), ")"
    score = 1
    for value in components[:-1]:
        if value <= 0:
            return 0, components[-1]
        score *= value
    return score, components[-1]

def possible_recipes(names, total_amount):
    for amount1 in range(1, total_amount+1):
        rest1 = total_amount - amount1
        for amount2 in range(1, rest1+1):
            rest2 = rest1 - amount2
            for amount3 in range(1, rest2+1):
                rest3 = rest2 - amount3
                for amount4 in range(1, rest3+1):
                    amount5 = rest3 - amount4
                    assert amount1+amount2+amount3+amount4+amount5 == total_amount
                    yield zip(names, [amount1, amount2, amount3, amount4, amount5])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        infile = sys.argv[1]

    with open(infile, "rb") as fp:
        input = fp.read()
    
    ingredients = load_input(input)
    print len(ingredients), "ingredients"
    print ", ".join(sorted(ingredients.keys()))
    print

    print "Part 1"
    recipes = []
    lowcal_recipes = []

    for recipe in possible_recipes(sorted(ingredients.keys()), total_amount):
        score, calories = score_recipe(recipe, ingredients)
        if score > 0:
            print "Score:", score, " Calories:",calories, " Recipe:", recipe
            recipes.append((score, calories, recipe))
            if calories == 500:
                lowcal_recipes.append((score, calories, recipe))

    recipes.sort(reverse=True)
    print
    for score, calories, recipe in recipes[:10]:
        print "Score:", score, " Calories:",calories, " Recipe:", recipe

    lowcal_recipes.sort(reverse=True)
    print
    for score, calories, recipe in lowcal_recipes[:10]:
        print "Score:", score, " Calories:",calories, " Recipe:", recipe


