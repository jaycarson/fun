#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Abilities import Ability


class AbilityTest(unittest.TestCase):
    def setUp(self):
        self.sut = Ability()

    def test_name(self):
        test_name = 'None'
        self.assertEqual(test_name, self.sut.name)


if __name__ == '__main__':
    unittest.main()
