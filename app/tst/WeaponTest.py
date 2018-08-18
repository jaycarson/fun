#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Weapon import Weapon
from Character import Character
from Clock import Clock

class WeaponTest(unittest.TestCase):
    def setUp(self):
        sut_skills = []
        sut_ability_set = {}
        sut_stats = {}
        sut_handed = []

        self.sut = Weapon(
            weapon_type='sword',
            quality='common',
            color='white',
            skills=sut_skills,
            handed=sut_handed,
            damage='slash',
            stats=sut_stats,
            ability_set=sut_ability_set,
            weapon_id=1
            )

    def test_get_weapon_type(self):
        self.assertEqual('sword', self.sut.get_weapon_type())