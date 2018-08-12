#!/usr/bin/python

from random import seed
from random import choice


class Enchantress(object):
    def __init__(self):
        self._magic_schools = [
            'Fire',
            'Earth',
            'Water',
            'Air',
            'Light',
            'Dark',
            'Life',
            'Death',
            'Illusion',
            'Hate',
        ]

        self._weapon_types = [
            'Axe',
            'Mace',
            'Sword',
            'Bow',
        ]

        self._book = BookSpell()

    def set_seed(self, new_seed):
        seed(new_seed)

    def enchant(self, weapon, magic_school='Any'):
        if magic_school == 'Any':
            magic_type = choice(self._magic_schools)
