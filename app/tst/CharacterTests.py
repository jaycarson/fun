#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Clock import Clock
from Character import Character
from Smithy import SmithWeapon
from Smithy import SmithArmor

from Library import BookStat


class CharacterTest(unittest.TestCase):
    def setUp(self):
        self._clock = Clock()
        self._book_stat = BookStat()
        new_stats = self._book_stat.generate_for_character()

        self.sut = Character(
            experience=0,
            race='human',
            name='sut',
            char_id=0,
            clock=self._clock,
            stats=new_stats
            )

    def test_starts_as_level_0(self):
        expected = 0
        self.assertEqual(expected, self.sut.get_level())

    def test_character_gains_a_level_level(self):
        expected = 1
        self.sut.give_experience(1001)
        self.assertEqual(expected, self.sut.get_level())

    def test_character_gains_a_level_test_skill_points_current(self):
        expected = 1
        self.sut.give_experience(1001)
        self.assertEqual(expected, self.sut.skillable.skill_points_current)

    def test_character_gains_a_level_test_skill_points_total(self):
        expected = 1
        self.sut.give_experience(1001)
        self.assertEqual(expected, self.sut.skillable.skill_points_total)

    def test_starts_with_no_experience(self):
        expected = 0
        self.assertEqual(expected, self.sut.get_experience())

    def test_character_gains_experience(self):
        starting = self.sut.get_experience()
        self.sut.give_experience(1001)
        ending = self.sut.get_experience()
        self.assertGreater(ending, starting)

    def test_gets_correct_id(self):
        expected_1 = 1
        expected_2 = 2
        sut_1 = Character(char_id=expected_1)
        sut_2 = Character(char_id=expected_2)
        self.assertEqual(expected_1, sut_1.char_id)
        self.assertEqual(expected_2, sut_2.char_id)

    def test_gets_name(self):
        expected = 'sut'
        self.assertEqual(expected, self.sut.name)

    def test_character_knows_the_worlds_time(self):
        test_time = 0
        self.assertEqual(test_time, self.sut.get_world_time())
        self._clock.increment_time()

    def test_character_still_knows_the_worlds_time(self):
        test_time = 1
        self._clock.increment_time()
        self.assertEqual(test_time, self.sut.get_world_time())

    def test_character_knows_the_locale_time(self):
        test_locale_id = 1
        test_time = 0
        self._clock.add_locale(locale_id=test_locale_id)
        self.sut.locale_id = test_locale_id
        self.assertEqual(test_time, self.sut.get_locale_time())

    def test_character_still_knows_the_locale_time(self):
        test_locale_id = 1
        test_time = 1
        self._clock.add_locale(locale_id=test_locale_id)
        self.sut.locale_id = test_locale_id
        self._clock.increment_locale_time(test_locale_id)
        self.assertEqual(test_time, self.sut.get_locale_time())

    def test_character_has_stats(self):
        base_stat = self._book_stat.get_base_stat()
        stat_list = self._book_stat.get_list()

        for stat in stat_list:
            self.assertEqual(base_stat, self.sut.get_stat(stat))

    def test_character_gets_a_weapon(self):
        weapon_smith = SmithWeapon()
        new_weapon = weapon_smith.create()
        weapon_id = self.sut.rack_weapon.give_weapon(new_weapon)
        self.sut.sets_weapon.equip_weapon_by_id(weapon_id=weapon_id)
        equiped_weapon = self.sut.sets_weapon.get_equiped_weapon()
        self.assertEqual(equiped_weapon, new_weapon)

    def test_character_gets_a_weapon_and_automatically_equips_it(self):
        weapon_smith = SmithWeapon()
        new_weapon = weapon_smith.create()
        self.sut.rack_weapon.give_weapon(new_weapon)
        equiped_weapon = self.sut.sets_weapon.get_equiped_weapon()
        self.assertEqual(equiped_weapon, new_weapon)

    def test_character_gets_an_armor_and_automatically_equips_it(self):
        armor_smith = SmithArmor()
        new_armor = armor_smith.create()
        piece = new_armor.piece
        self.sut.rack_armor.give_armor(new_armor)
        equiped_armor = self.sut.rack_armor.get_equiped_armor(piece)
        self.assertEqual(equiped_armor, new_armor)


class CharacterCombatTest(unittest.TestCase):
    def setUp(self):
        locale_id = 5000
        self._clock = Clock()
        self._clock.add_locale(locale_id=locale_id, local_time=5)
        self._book_stat = BookStat()
        new_stats = self._book_stat.generate_for_character()

        self.sut = Character(
            experience=0,
            race='human',
            name='sut',
            char_id=0,
            clock=self._clock,
            stats=new_stats
            )

        self.sut.locale_id = locale_id

        weapon_smith = SmithWeapon()
        new_weapon = weapon_smith.create()
        self.sut.rack_weapon.give_weapon(new_weapon)

    def test_weapon_starts_off_cooldown(self):
        weapon = self.sut.sets_weapon.get_equiped_weapon()
        slot = 2
        self._clock.increment_locale_time(self.sut.locale_id)
        locale_time = self._clock.get_locale_time(self.sut.locale_id)
        self.assertFalse(weapon.on_cooldown(slot, locale_time))

    def test_weapon_goes_on_cooldown(self):
        weapon = self.sut.sets_weapon.get_equiped_weapon()
        slot = 2
        self._clock.increment_locale_time(self.sut.locale_id)
        self.sut.attack(slot)
        locale_time = self._clock.get_locale_time(self.sut.locale_id)
        self.assertTrue(weapon.on_cooldown(slot, locale_time))


if __name__ == '__main__':
    unittest.main()
