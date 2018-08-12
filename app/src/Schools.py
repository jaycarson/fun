#!/usr/bin/python

from Weapon import Weapon
from Ability import Ability
from TokenSet import TokenSet
from random import choice


class School(object):
    def __init__(self):
        self._school_name = 'None'

        self._weapon_types = [
            'Bludgeon',
            'Chop',
            'Pierce',
            'Slash',
        ]

        self._weapon_spells = {
            'Bludgeon': [],
            'Chop': [],
            'Pierce': [],
            'Slash': [],
        }

    def get_weapon_abilities(self, weapon='Any'):
        if weapon == 'Any':
            weapon = choice(self._weapon_types)

        return self._weapon_spells[weapon]


class SchoolAir(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Air'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolDarkness(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Darkness'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolDeath(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Death'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolEarth(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Earth'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolEngineer(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Engineer'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolFinesse(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Finesse'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolFire(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Fire'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolHate(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Hate'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolHunt(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Hunt'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolLife(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Life'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolLight(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Light'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolMartial(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Martial'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
                AbilitySeverArtery(),
                AbilityGash(),
                AbilityHamstring(),
                AbilitySavageLeap(),
                AbilityFinalThrust(),
                AbilityImpale(),
                AbilityRip(),
                AbilityRipost(),
                AbilityRush(),
            ],
            'Pierce': [
            ],
        }


class SchoolSimple(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Simple'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }


class SchoolWater(School):
    def __init__(self):
        School.__init__(self)
        self._school_name = 'Water'

        self._weapon_spells = {
            'Bludgeon': [
            ],
            'Chop': [
            ],
            'Slash': [
            ],
            'Pierce': [
            ],
        }
