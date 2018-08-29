#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Clock import Clock
from Faction import Faction
from Smithy import SmithWeapon
from Smithy import SmithArmor



class FactionTest(unittest.TestCase):
    def setUp(self):
        self._clock = Clock()

        self.sut = Faction(
            experience=0,
            race='human',
            name='sut',
            faction_id=0,
            clock=self._clock,
            )

    def test_starts_as_level_0(self):
        expected = 0
        self.assertEqual(expected, self.sut.get_level())

    def test_faction_gains_a_level_level(self):
        expected = 1
        self.sut.give_experience(1001)
        self.assertEqual(expected, self.sut.get_level())

    def test_faction_gains_a_level_test_skill_points_current(self):
        expected = 1
        self.sut.give_experience(1001)
        self.assertEqual(expected, self.sut.skill_points_current)

    def test_faction_gains_a_level_test_skill_points_total(self):
        expected = 1
        self.sut.give_experience(1001)
        self.assertEqual(expected, self.sut.skill_points_total)

    def test_starts_with_no_experience(self):
        expected = 0
        self.assertEqual(expected, self.sut.experience)

    def test_faction_gains_experience(self):
        starting = self.sut.experience
        self.sut.give_experience(1001)
        ending = self.sut.experience
        self.assertGreater(ending, starting)

    def test_gets_correct_id(self):
        expected_1 = 1
        expected_2 = 2
        sut_1 = Faction(faction_id=expected_1)
        sut_2 = Faction(faction_id=expected_2)
        self.assertEqual(expected_1, sut_1.faction_id)
        self.assertEqual(expected_2, sut_2.faction_id)

    def test_gets_name(self):
        expected = 'sut'
        self.assertEqual(expected, self.sut.name)

    def test_faction_knows_the_worlds_time(self):
        test_time = 0
        self.assertEqual(test_time, self.sut.get_world_time())
        self._clock.increment_time()

    def test_faction_still_knows_the_worlds_time(self):
        test_time = 1
        self._clock.increment_time()
        self.assertEqual(test_time, self.sut.get_world_time())


if __name__ == '__main__':
    unittest.main()
