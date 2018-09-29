#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Clock import Clock
from Faction import Faction
from Smithy import Smithy

from Library import Library


class FactionTest(unittest.TestCase):
    def setUp(self):
        self._clock = Clock()
        self.sut_name = 'sut'
        self.library = Library()
        self.sut_smithy = Smithy(self.library)
        self.sut_smithy_weapon = self.sut_smithy.get_smith('weapon')
        self.sut_smithy_armor = self.sut_smithy.get_smith('armor')

        self.sut = Faction(
            experience=0,
            name=self.sut_name,
            faction_id=0,
            clock=self._clock,
            smithy=self.sut_smithy,
            library=self.library,
            )

    def test_starts_as_level_0(self):
        expected = 0
        self.assertEqual(expected, self.sut.levelable.get_level())

    def test_faction_gains_a_level_level(self):
        expected = 1
        self.sut.give_experience(1001)
        self.assertEqual(expected, self.sut.levelable.get_level())

    def test_faction_gains_a_level_test_skill_points_current(self):
        expected = 1
        self.sut.give_experience(1001)
        self.assertEqual(expected, self.sut.skillable.skill_points_current)

    def test_faction_gains_a_level_test_skill_points_total(self):
        expected = 1
        self.sut.give_experience(1001)
        self.assertEqual(expected, self.sut.skillable.skill_points_total)

    def test_starts_with_no_experience(self):
        expected = 0
        self.assertEqual(expected, self.sut.get_experience())

    def test_faction_gains_experience(self):
        starting = self.sut.get_experience()
        self.sut.give_experience(1001)
        ending = self.sut.get_experience()
        self.assertGreater(ending, starting)

    def test_gets_correct_id(self):
        expected_1 = 1
        expected_2 = 2
        sut_1 = Faction(
                faction_id=expected_1,
                library=self.library,
                smithy=self.sut_smithy,
            )
        sut_2 = Faction(
                faction_id=expected_2,
                library=self.library,
                smithy=self.sut_smithy,
            )
        self.assertEqual(expected_1, sut_1.faction_id)
        self.assertEqual(expected_2, sut_2.faction_id)

    def test_gets_name(self):
        self.assertEqual(self.sut_name, self.sut.name)

    def test_faction_knows_the_worlds_time(self):
        test_time = 0
        self.assertEqual(test_time, self.sut.get_world_time())
        self._clock.increment_time()

    def test_faction_still_knows_the_worlds_time(self):
        test_time = 1
        self._clock.increment_time()
        self.assertEqual(test_time, self.sut.get_world_time())

    def test_faction_receives_a_weapon(self):
        colors = self.library.get_book('color').get_list()
        new_weapon = self.sut_smithy_weapon.create()
        self.sut.rack_weapon.give_weapon(new_weapon)
        given_wpn = self.sut.rack_weapon.weapons[new_weapon.id]
        self.assertTrue(given_wpn.color in colors)

    def test_faction_receives_an_armor(self):
        colors = self.library.get_book('color').get_list()
        armor_smith = self.sut_smithy.get_smith('armor')
        new_armor = armor_smith.create()
        self.sut.rack_armor.give_armor(new_armor)
        given_arm = self.sut.rack_armor.armors[new_armor.id]
        self.assertTrue(given_arm.color in colors)

    def test_created_character_gets_a_weapon(self):
        vpc = self.sut.create_vpc()


if __name__ == '__main__':
    unittest.main()
