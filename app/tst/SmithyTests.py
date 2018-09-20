#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Smithy import Smithy
from Smithy import Smith
from Smithy import SmithArmor
from Smithy import SmithWeapon

from Library import Library

class SmithTest(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.sut = Smith(library=self.library)

    def test_generate_color(self):
        book_color = self.library.get_book('color')
        colors = book_color.get_list()
        self.assertTrue(self.sut.generate_color() in colors)


class SmithArmorTest(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.sut = SmithArmor(library=self.library)

    def test_generate_color(self):
        book_color = self.library.get_book('color')
        colors = book_color.get_list()
        self.assertTrue(self.sut.generate_color() in colors)

    def test_create_check_type(self):
        armor_types = self.library.get_book('armor').get_types()

        armor = self.sut.create()
        self.assertTrue(armor.armor_type in armor_types)

    def test_create_check_piece(self):
        armor_pieces = self.library.get_book('armor').get_pieces()

        armor = self.sut.create()
        self.assertTrue(armor.piece in armor_pieces)

    def test_create_check_quality(self):
        qualities = self.library.get_book('quality').get_list()

        armor = self.sut.create()
        self.assertTrue(armor.quality in qualities)

    def test_create_check_color(self):
        colors = self.library.get_book('color').get_list()

        armor = self.sut.create()
        self.assertTrue(armor.color in colors)


class SmithWeaponTest(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.sut = SmithWeapon(self.library)

    def test_generate_color(self):
        book_color = self.library.get_book('color')
        colors = book_color.get_list()
        self.assertTrue(self.sut.generate_color() in colors)

    def test_create_check_type(self):
        weapon_types = self.library.get_book('weapon').get_weapons()
        weapon = self.sut.create()
        self.assertTrue(weapon.weapon_type in weapon_types)

    def test_create_check_quality(self):
        qualities = self.library.get_book('quality').get_list()
        weapon = self.sut.create()
        self.assertTrue(weapon.quality in qualities)

    def test_create_check_color(self):
        colors = self.library.get_book('color').get_list()
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
