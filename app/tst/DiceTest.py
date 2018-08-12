#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Dice import Dice


class DiceTest(unittest.TestCase):
    def setUp(self):
        self.sut = Dice(1, 2, 3)

    def test_roll_the_dice(self):
        self.sut.set_seed(0)
        self.assertEqual("Morale", self.sut.roll())
        self.sut.set_seed(1)
        self.assertEqual("Attack", self.sut.roll())
        self.sut.set_seed(2)
        self.assertEqual("Morale", self.sut.roll())
        self.sut.set_seed(3)
        self.assertEqual("Defense", self.sut.roll())
        self.sut.set_seed(4)
        self.assertEqual("Defense", self.sut.roll())

    def test_set_attack(self):
        self.sut.set_attack()
        self.assertEqual("Attack", self.sut.get_value())

    def test_set_defense(self):
        self.sut.set_defense()
        self.assertEqual("Defense", self.sut.get_value())

    def test_set_morale(self):
        self.sut.set_morale()
        self.assertEqual("Morale", self.sut.get_value())


if __name__ == '__main__':
    unittest.main()
