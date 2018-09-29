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

        self.sut = Weapon()
        self.sut.weapon_type = 'sword'
        self.sut.quality = 'common'
        self.sut.color = 'white'
        self.sut.skills = sut_skills
        self.sut.handed = sut_handed
        self.sut.damage = 'slash'
        self.sut.stats = sut_stats
        self.sut.ability_set = sut_ability_set
        self.sut.cd_timer_set = sut_cooldown_set
        self.sut.strength_set = sut_strength_set
        self.sut.weapon_id = 1
        self.sut.add_dice(Dice(attack=2, defense=2, morale=2))

    def test_get_weapon_type(self):
        self.assertEqual('sword', self.sut.weapon_type)


if __name__ == '__main__':
    unittest.main()
