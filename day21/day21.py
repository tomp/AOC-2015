#!/usr/bin/env python

from itertools import combinations

class Item(object):
    def __init__(self, name, cost, damage, armor):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor

weapons = [ Item("Dagger", 8, 4, 0),
            Item("Shortsword", 10, 5, 0),
            Item("Warhammer", 25, 6, 0),
            Item("Longsword", 40, 7, 0),
            Item("Greataxe", 74, 8, 0) ]

armors = [ Item("Leather", 13, 0, 1),
           Item("Chainmail", 31, 0, 2),
           Item("Splintmail", 53, 0, 3),
           Item("Bandedmail", 75, 0, 4),
           Item("Platemail", 102, 0, 5) ]

rings = [ Item("Damage +1", 25, 1, 0),
          Item("Damage +2", 50, 2, 0),
          Item("Damage +3", 100, 3, 0),
          Item("Defense +1", 20, 0, 1),
          Item("Defense +2", 40, 0, 2),
          Item("Defense +3", 80, 0, 3) ]

class Player(object):
    def __init__(self, name, hitpoints, damage=0, armor=0, gold=0,
            inventory=None):
        self.name = name
        self._hitpoints = hitpoints
        self._damage = damage
        self._armor = armor
        self._gold = gold
        self.restore()
        if inventory is not None:
            for item in inventory:
                self.pick_up(item)

    def restore(self):
        self.health = self._hitpoints
        self.armor = self._armor
        self.damage = self._damage
        self.gold = self._gold
        self.equipment = []
        self.inventory_value = 0

    def restore_health(self):
        self.health = self._hitpoints

    def pick_up(self, item):
        self.equipment.append(item)
        self.armor += item.armor
        self.damage += item.damage
        self.inventory_value += item.cost

    def attacked(self, opponent):
        """
        Player is attacked by given opponent.
        Returns True if player survives the attack, False if he's killed.
        """
        if self.health < 1:
            print "Dead player {} is attacked by {}".format(self.name, opponent.name)
            return False
        power = opponent.damage - self.armor
        if power < 1:
            power = 1
        self.health -= power
        if self.health < 0:
            self.health = 0
        print "{} receives {} damage from {} ({} hit points left)".format(
                self.name, power, opponent.name, self.health)
        return self.is_alive()

    def would_defeat(self, opponent):
        """
        Evaluate who would win a fight to the death between the player
        and the given opponent, with the player striking first.
        Return True if the player would win, false if the opponent would win.
        """
        if opponent.damage > self.armor:
            damage_received = opponent.damage - self.armor
        else:
            damage_received = 1

        if self.damage > opponent.armor:
            damage_given = self.damage - opponent.armor
        else:
            damage_given = 1

        blows_received = (self.health + damage_received - 1) // damage_received
        blows_given = (opponent.health + damage_given - 1) // damage_given
        # print "[blows given: {}, blows received: {}]".format(blows_given, blows_received)
        return blows_given <= blows_received

    def is_alive(self):
        return self.health > 0


def next_equipment(weapons, armors, rings):
    for weapon in weapons:
        for armor in armors:
            yield([weapon, armor])
    for ring in rings:
        for weapon in weapons:
            for armor in armors:
                yield([weapon, armor, ring])
    for ring1, ring2 in combinations(rings, 2):
        for weapon in weapons:
            for armor in armors:
                yield([weapon, armor, ring1, ring2])

if __name__ == '__main__':

    print "Warm up"
    boss = Player("Boss", 12, damage=7, armor=2)
    you = Player("You", 8, damage=5, armor=5)

    if you.would_defeat(boss):
        print "You should defeat the boss."
    else:
        print "You should lose."
    print

    while you.is_alive():
        if boss.attacked(you):
            you.attacked(boss)
        else:
            break

    if you.is_alive():
        print "You win!"
    else:
        print "Boss wins!"
    print

    print "Part 1"
    print "(What's the least you can spend to win?)"
    
    boss = Player("Boss", 103, damage=9, armor=2)

    results = []
    for items in next_equipment(weapons, armors, rings):
        you = Player("You", 100, inventory=items)
        if you.would_defeat(boss):
            results.append((you.inventory_value, tuple(you.equipment)))
    
    print
    results.sort()
    for cost, equipment in results[:5]:
        print "Cost: {}  Inventory: {}".format(cost,
                ", ".join(item.name for item in equipment))


    print
    print "Part 2"
    print "(How much can you spend and still lose?)"

    results = []
    for items in next_equipment(weapons, armors, rings):
        you = Player("You", 100, inventory=items)
        if boss.would_defeat(you):
            results.append((you.inventory_value, tuple(you.equipment)))
    
    print
    results.sort(reverse=True)
    for cost, equipment in results[:5]:
        print "Cost: {}  Inventory: {}".format(cost,
                ", ".join(item.name for item in equipment))

