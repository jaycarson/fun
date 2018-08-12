#!/usr/bin/python

import random


class Dice(object):
    def __init__(self, attack=2, defense=2, morale=2):
        self._attack = attack
        self._defense = defense + attack
        self._morale = morale + self._defense
        self._sides = self._morale
        self._value = "Attack"

    def set_seed(self, seed):
        random.seed(seed)

    def set_attack(self):
        self._value = "Attack"

    def set_defense(self):
        self._value = "Defense"

    def set_morale(self):
        self._value = "Morale"

    def get_value(self):
        return self._value

    def roll(self):
        n = random.randint(0, self._sides)

        if n < self._attack:
            self._value = "Attack"
        elif n < self._defense:
            self._value = "Defense"
        else:
            self._value = "Morale"

        return self._value


if __name__ == "__main__":
    dice = Dice()

    for x in range(0, 5):
        dice.set_seed(x)
        roll = dice.roll()
        print roll
