#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Abilities import Ability
from StatusEffect import StatusEffects
from Library import Library


class AbilityTest(unittest.TestCase):
    def setUp(self):
        library = Library()
        self.sut = Ability(library)

    def test_name(self):
        test_name = 'None'
        self.assertEqual(test_name, self.sut.name_1)


if __name__ == '__main__':
    unittest.main()
