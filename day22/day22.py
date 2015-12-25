#!/usr/bin/env python

import sys
from itertools import combinations
import heapq

import logging
log = logging.getLogger("day22")
log.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter("%(message)s"))
log.addHandler(console)

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

class Spell(object):
    """
    A Spell represents the basic characteristics of a spell that
    can be cast by a wizard.

    cost ...... the cost in gold to the wizard to use the spell.
    damage .... the immediate damage done to the target when cast.
    turns ..... the number of turns that the spells effects apply.
                (This is zero if the spells only effects are immediate.)
    """
    def __init__(self, name, cost, turns=0):
        self.name = name
        self.cost = cost
        self.turns = turns

MISSILE_SPELL = Spell("Magic Missile", 53)
MISSILE_DAMAGE = 4

DRAIN_SPELL = Spell("Drain", 73)
DRAIN_HEALING = 2
DRAIN_DAMAGE = 2

POISON_SPELL = Spell("Poison", 173, turns=6)
POISON_DAMAGE = 3

RECHARGE_SPELL = Spell("Recharge", 229, turns=5)
RECHARGE_AMOUNT = 101

SHIELD_SPELL = Spell("Shield", 113, turns=6)
SHIELD_ENHANCEMENT = 7

# Available spells, in order of increasing cost
all_spells = (MISSILE_SPELL, DRAIN_SPELL, SHIELD_SPELL, POISON_SPELL, RECHARGE_SPELL)

class Player(object):
    def __init__(self, name, hitpoints, damage=0, armor=0, gold=0, mana=0,
            inventory=None):
        # Set intrinisic attributes of player
        self.name = name
        self._hitpoints = hitpoints
        self._damage = damage
        self._armor = armor
        # Set variable attributes
        self.reset()
        self.gold = gold
        self.mana = mana
        if inventory is not None:
            for item in inventory:
                self.pick_up(item)

    def reset(self):
        self.health = self._hitpoints
        self.armor = self._armor
        self.damage = self._damage
        self.gold = 0
        self.mana = 0
        self.inventory = []
        self.under_poison = 0
        self.under_recharge = 0
        self.under_shield = 0

    def pick_up(self, item):
        """
        Add the given item to the player's inventory.
        Update the player's armor and damage to reflect the new item.
        """
        self.inventory.append(item)
        self.armor += item.armor
        self.damage += item.damage

    def inventory_value(self):
        return sum([item.cost for item in self.inventory])

    def effective_armor(self):
        if self.under_shield:
            return self.armor + SHIELD_ENHANCEMENT
        else:
            return self.armor

    # On each turn, a player is expected to either attack or to cast a spell.
    # Start-of-turn logic is therefor built into these methods.
    def attack(self, opponent):
        if self.is_alive():
            opponent._attacked(self)

    def cast_spell(self, spell, opponent=None):
        assert spell.cost <= self.mana
        if self.is_alive():
            self.mana -= spell.cost
            log.debug("{} casts {} spell ({} mana left)".format(self.name,
                    spell.name, self.mana))
            if spell in (MISSILE_SPELL, DRAIN_SPELL, POISON_SPELL):
                assert opponent is not None
                opponent._spell_cast(spell)
                if spell == DRAIN_SPELL:
                    self.health += DRAIN_HEALING
            if spell in (SHIELD_SPELL, RECHARGE_SPELL):
                self._spell_cast(spell)
            

    def _attacked(self, opponent):
        """
        Player is attacked by given opponent.
        Returns True if player survives the attack, False if he's killed.
        """
        if self.health < 1:
            log.debug("Dead player {} is attacked by {}".format(self.name, opponent.name))
            return False
        power = opponent.damage - self.effective_armor()
        if power < 1:
            power = 1
        self._damage_received(power)
        return self.is_alive()

    def _damage_received(self, damage, cause="blow"):
        if self.health >= damage:
            self.health -= damage
        else:
            self.health = 0
        log.debug("{} receives {} damage from {} ({} hit points left)".format(
                self.name, damage, cause, self.health))
        return self.is_alive()

    def _spell_cast(self, spell):
        if self.health < 1:
            log.debug("Dead player {} receives {} spell".format(self.name, spell.name))
            return False
        else:
            log.debug("{} receives {} spell".format(self.name, spell.name))
        if spell == MISSILE_SPELL:
            return self._damage_received(MISSILE_DAMAGE, spell.name)
        elif spell == DRAIN_SPELL:
            return self._damage_received(DRAIN_DAMAGE, spell.name)
        elif spell == SHIELD_SPELL:
            if not self.under_shield:
                self.under_shield = spell.turns
        elif spell == POISON_SPELL:
            if not self.under_poison:
                self.under_poison = spell.turns
        elif spell == RECHARGE_SPELL:
            if not self.under_recharge:
                self.under_recharge = spell.turns

    def apply_spell_effects(self):
        if self.under_poison:
            self._damage_received(POISON_DAMAGE, POISON_SPELL.name)
            self.under_poison -= 1
        if self.under_recharge:
            self.mana += RECHARGE_AMOUNT
            self.under_recharge -= 1
            log.debug("{} receives {} mana from {} ({} mana left)".format(
                    self.name, RECHARGE_AMOUNT, RECHARGE_SPELL.name, self.mana))
        if self.under_shield:
            self.under_shield -= 1

    def would_defeat(self, opponent):
        """
        Evaluate who would win a fight to the death between the player
        and the given opponent, with the player striking first. (No magic.)
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
        # log.debug("[blows given: {}, blows received: {}]".format(blows_given, blows_received))
        return blows_given <= blows_received

    def is_alive(self):
        return self.health > 0

def run_scenario(player, boss, spell_queue=[], deathmatch=True, hardmode=False):
    """
    Run battle between player and opponent destructively.
    (Input arguments are modified by play.)
    """
    while True:
        boss.apply_spell_effects()
        if not boss.is_alive():
            break

        player.apply_spell_effects()
        if hardmode:
            player._damage_received(1, "hard mode")
        if not player.is_alive():
            break

        if spell_queue:
            player.cast_spell(spell_queue.pop(0), boss)
        elif not deathmatch:
            return

        log.debug("")
        player.apply_spell_effects()
        boss.apply_spell_effects()
        if not boss.is_alive():
            break

        boss.attack(player)
        if not player.is_alive():
            break
        log.debug("")

def report_winner(player, boss):
    if player.is_alive():
        print "{} wins!".format(player.name)
    else:
        print "{} wins!".format(boss.name)

def next_equipment(weapons, armors, rings):
    """
    A generator that returns every possible combination of weapon, armor,
    and rings that a player could purchase.
    """
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

def legal_spell(spell, seq):
    if spell.turns < 3:
        return True
    window = (spell.turns - 1) // 2
    if len(seq) > window:
        return spell not in seq[-window:]
    else:
        return spell not in seq

def cheapest_winning_spell_sequence(player_hitpoints=0, player_mana=0,
        boss_hitpoints=0, boss_damage=0, spells=None, hardmode=False):
    """
    Report the least expensive sequence of spells that defeat the boss, for the
    given player and boss attributes.

    A tuple of (cost, spell list) is returned.
    """
    assert spells is not None and len(spells) > 0

    fringe = []
    for s in spells:
        if s.cost <= player_mana:
            heapq.heappush(fringe, (s.cost, [s], player_mana - s.cost))

    while True:
        cost, seq, mana = heapq.heappop(fringe)
        you = Player("Player", hitpoints=player_hitpoints, mana=player_mana)
        boss = Player("Boss", hitpoints=boss_hitpoints, damage=boss_damage)
        run_scenario(you, boss, list(seq), deathmatch=False, hardmode=hardmode)
        if not boss.is_alive():
            return (cost, seq)

        if you.is_alive() and ((you.health // 3) + 1 >= (boss.health // 6)):
            if boss.health < 13:
                print "Cost: {:4d}  You: {} hp, {} mana  Boss: {} hp  Spells: {}".format(
                        cost, you.health, you.mana, boss.health, ", ".join( [s.name for s in seq]))
            for s in spells:
                if s.cost <= you.mana and legal_spell(s, seq):
                    heapq.heappush(fringe, (cost + s.cost, seq + [s], you.mana - s.cost))


if __name__ == '__main__':

    print "Day 21: Warm up"
    boss = Player("Boss", 12, damage=7, armor=2)
    you = Player("Player", 8, damage=5, armor=5)

    if you.would_defeat(boss):
        print "Player should defeat the boss."
    else:
        print "Player should lose."
    print

    run_scenario(you, boss)
    report_winner(you, boss)
    print

    print "Day 21: Part 1"
    print "(What's the least you can spend to win?)"
    
    boss = Player("Boss", 103, damage=9, armor=2)

    results = []
    for items in next_equipment(weapons, armors, rings):
        you = Player("Player", 100, inventory=items)
        if you.would_defeat(boss):
            results.append((you.inventory_value(), tuple(you.inventory)))
    
    print
    results.sort()
    for cost, inventory in results[:5]:
        print "Cost: {}  Inventory: {}".format(cost,
                ", ".join(item.name for item in inventory))

    print
    print "Day 21: Part 2"
    print "(How much can you spend and still lose?)"

    results = []
    for items in next_equipment(weapons, armors, rings):
        you = Player("Player", 100, inventory=items)
        if boss.would_defeat(you):
            results.append((you.inventory_value(), tuple(you.inventory)))
    
    print
    results.sort(reverse=True)
    for cost, inventory in results[:5]:
        print "Cost: {}  Inventory: {}".format(cost,
                ", ".join(item.name for item in inventory))

    print
    print "Day 22: Warm up (scenario 1)"
    boss = Player("Boss", hitpoints=13, damage=8, armor=2)
    you = Player("Player", hitpoints=10, mana=250)
    spell_sequence = [POISON_SPELL, MISSILE_SPELL]
    run_scenario(you, boss, spell_sequence)
    report_winner(you, boss)
    print

    print
    print "Day 22: Warm up (scenario 2)"
    boss = Player("Boss", hitpoints=14, damage=8, armor=2)
    you = Player("Player", hitpoints=10, mana=250)
    spell_sequence = [RECHARGE_SPELL, SHIELD_SPELL, DRAIN_SPELL, POISON_SPELL, MISSILE_SPELL]
    run_scenario(you, boss, spell_sequence)
    report_winner(you, boss)
    print

    print
    print "Day 22: Part 2 test"
    boss = Player("Boss", hitpoints=71, damage=10)
    you = Player("Player", hitpoints=50, mana=500)
    spell_sequence = [SHIELD_SPELL, RECHARGE_SPELL, POISON_SPELL, SHIELD_SPELL, RECHARGE_SPELL, POISON_SPELL, SHIELD_SPELL, RECHARGE_SPELL, POISON_SPELL, SHIELD_SPELL, DRAIN_SPELL, POISON_SPELL, MISSILE_SPELL]
    run_scenario(you, boss, spell_sequence)
    report_winner(you, boss)
    print

    print "Day 22: Part 1"
    log.setLevel(logging.INFO)

    boss_hitpoints = 71
    boss_damage = 10
    player_hitpoints = 50
    player_mana = 500

    try:
        cost, seq = cheapest_winning_spell_sequence(player_hitpoints, player_mana,
                boss_hitpoints, boss_damage, spells=all_spells, hardmode=False)
        print "* * * * * * * * * * * * * * * * *"
        print "Cost: {:4d}  Spells: {}".format(cost, ", ".join( [s.name
            for s in seq]))
    except Exception as exc:
        print "Search failed!"
        raise exc

    print
    print "Day 22: Part 2"

    try:
        cost, seq = cheapest_winning_spell_sequence(player_hitpoints, player_mana,
                boss_hitpoints, boss_damage, spells=all_spells, hardmode=True)
        print "* * * * * * * * * * * * * * * * *"
        print "Cost: {:4d}  Spells: {}".format(cost, ", ".join( [s.name
            for s in seq]))
    except Exception as exc:
        print "Search failed!"
        raise exc

