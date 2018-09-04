#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Smithy import Smithy
from Smithy import Smith
from Smithy import SmithArmor
from Smithy import SmithWeapon

from Library import BookColor
from Library import BookArmor
from Library import BookWeapon
from Library import BookQuality

class SmithTest(unittest.TestCase):
    def setUp(self):
        self.sut = Smith()

    def test_generate_color(self):
        book_color = BookColor()
        colors = book_color.get_list()
        self.assertTrue(self.sut.generate_color() in colors)


class SmithArmorTest(unittest.TestCase):
    def setUp(self):
        self.sut = SmithArmor()

    def test_generate_color(self):
        book_color = BookColor()
        colors = book_color.get_list()
        self.assertTrue(self.sut.generate_color() in colors)

    def test_create_check_type(self):
        armor_types = BookArmor().get_types()

        armor = self.sut.create()
        self.assertTrue(armor.armor_type in armor_types)

    def test_create_check_piece(self):
        armor_pieces = BookArmor().get_pieces()

        armor = self.sut.create()
        self.assertTrue(armor.piece in armor_pieces)

    def test_create_check_quality(self):
        qualities = BookQuality().get_list()

        armor = self.sut.create()
        self.assertTrue(armor.quality in qualities)

    def test_create_check_color(self):
        colors = BookColor().get_list()

        armor = self.sut.create()
        self.assertTrue(armor.color in colors)


class SmithWeaponTest(unittest.TestCase):
    def setUp(self):
        self.sut = SmithWeapon()

    def test_generate_color(self):
        book_color = BookColor()
        colors = book_color.get_list()
        self.assertTrue(self.sut.generate_color() in colors)

    def test_create_check_type(self):
        weapon_types = BookWeapon().get_weapons()
        weapon = self.sut.create()
        self.assertTrue(weapon.weapon_type in weapon_types)

    def test_create_check_quality(self):
        qualities = BookQuality().get_list()
        weapon = self.sut.create()
        self.assertTrue(weapon.quality in qualities)

    def test_create_check_color(self):
        colors = BookColor().get_list()
        weapon = self.sut.create()
        self.assertTrue(weapon.color in colors)

    def test_weapon_got_five_abilities(self):
        weapon = self.sut.create()
        expected_quantity_of_abilities = 5
        self.assertEqual(
            expected_quantity_of_abilities, 
            len(weapon.get_active_ability_set())
        )


if __name__ == '__main__':
    unittest.main()
