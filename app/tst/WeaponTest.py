#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Weapon import Weapon
from Character import Character
from Clock import Clock
from Dice import Dice

class WeaponTest(unittest.TestCase):
    def setUp(self):
        sut_skills = []
        sut_ability_set = {}
        sut_cooldown_set = {}
        sut_cooldown_adj_set = {}
        sut_strength_set = {}
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
            cd_timer_set=sut_cooldown_set,
            cd_adj_set=sut_cooldown_adj_set,
            strength_set=sut_strength_set,
            weapon_id=1,
            dice=Dice(attack=2, defense=2, morale=2)
            )

    def test_get_weapon_type(self):
        self.assertEqual('sword', self.sut.weapon_type)


if __name__ == '__main__':
    unittest.main()
