#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Clock import Clock
from Character import Character
from Faction import Faction
from Smithy import Smithy, SmithWeapon, SmithArmor
from HexMap import HexMap
from DungeonMaster import DungeonMaster
from Brain import Brains

from Library import Library


class RegimentTest(unittest.TestCase):
    def setUp(self):
        self._clock = Clock()
        self.locale_id = 1000
        self.library = Library()
        self.book_stat = self.library.get_book('stat')
        self.sut_smithy = Smithy(self.library)
        self.sut_brains = Brains()

        self.sut_faction = Faction(
                    experience=0,
                    name='Red',
                    faction_id='1000',
                    clock=self._clock,
                    smithy=self.sut_smithy,
                    brains=self.sut_brains,
                    library=self.library
                )

        self.sut_vpc = self.sut_faction.create_vpc(name='sut_vpc')
        self.sut = self.sut_faction.create_regiment(
                    name='sut',
                    owner=self.sut_vpc,
                )

        arena = HexMap()
        arena.arena_ground = 'plains'
        arena.arena_height = 10
        arena.create_arena(radius=5)

        self.sut_dm = DungeonMaster(
                clock=Clock(),
                dungeon=arena,
                locale_id=self.locale_id,
                library=self.library,
            )

        self.sut_dm.add_unit(
                member=self.sut,
                faction=self.sut_faction,
                edge='sw',
            )

    def test_starts_as_level_0(self):
        expected = 0
        self.assertEqual(expected, self.sut.get_level())

    def test_regiment_starts_with_ten_soldiers(self):
        expected = 10
        self.assertEqual(expected, self.sut.size)

    def test_regiment_increases(self):
        expected = 11
        self.sut.add_unit(quantity=1)
        self.assertEqual(expected, self.sut.size)

    def test_regiment_honors_max(self):
        max_size = 15
        self.sut.max_size = max_size
        self.sut.add_unit(quantity=45)
        self.assertEqual(max_size, self.sut.size)

    def test_initial_formation_depth(self):
        expected = 3
        self.assertEqual(expected, self.sut.formation_depth)

    def test_front_of_unit_takes_damage(self):
        self.sut.take_damage_front(
                damage=10,
                target_count=4,
            )

        expected = [
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health,
            ]

        actual = []

        for soldier in self.sut.soldiers:
            actual.append(soldier.health)

        self.assertEqual(expected, actual)

    def test_front_two_ranks_of_unit_takes_damage(self):
        self.sut.take_damage_front(
                damage=10,
                target_count=8,
            )

        expected = [
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health,
                self.sut.max_health,
            ]

        actual = []

        for soldier in self.sut.soldiers:
            actual.append(soldier.health)

        self.assertEqual(expected, actual)

    def test_unit_takes_damage_from_front(self):
        self.sut.take_damage_front(
                damage=10,
                target_count=30,
            )

        expected = [
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
            ]

        actual = []

        for soldier in self.sut.soldiers:
            actual.append(soldier.health)

        self.assertEqual(expected, actual)

    def test_unit_takes_damage_from_right_side(self):
        self.sut.take_damage_right_side(
                damage=10,
                target_count=30,
            )

        expected = [
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
            ]

        actual = []

        for soldier in self.sut.soldiers:
            actual.append(soldier.health)

        self.assertEqual(expected, actual)

    def test_unit_takes_damage_from_rear(self):
        self.sut.take_damage_rear(
                damage=10,
                target_count=30,
            )

        expected = [
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
                self.sut.max_health - 10 * 3,
            ]

        actual = []

        for soldier in self.sut.soldiers:
            actual.append(soldier.health)

        self.assertEqual(expected, actual)

    def test_back_of_unit_takes_damage(self):
        self.sut.take_damage_rear(
                damage=10,
                target_count=4,
            )

        expected = [
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
            ]

        actual = []

        for soldier in self.sut.soldiers:
            actual.append(soldier.health)

        self.assertEqual(expected, actual)

    def test_right_of_unit_takes_damage(self):
        self.sut.take_damage_right_side(
                damage=10,
                target_count=4,
            )

        expected = [
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health,
                self.sut.max_health,
            ]

        actual = []

        for soldier in self.sut.soldiers:
            actual.append(soldier.health)

        self.assertEqual(expected, actual)

    def test_left_of_unit_takes_damage(self):
        self.sut.take_damage_left_side(
                damage=10,
                target_count=4,
            )

        expected = [
                self.sut.max_health - 10 * 1,
                self.sut.max_health - 10 * 1,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health - 10 * 1,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health,
                self.sut.max_health - 10 * 1,
                self.sut.max_health,
            ]

        actual = []

        for soldier in self.sut.soldiers:
            actual.append(soldier.health)

        self.assertEqual(expected, actual)

    def test_soldier_can_die(self):
        starting_size = 10
        self.assertEqual(starting_size, self.sut.size)

        self.sut.take_damage_front(
                damage=100000,
                target_count=1,
            )
        self.sut.resolve_unit_damage()

        self.assertEqual(starting_size - 1, self.sut.size)
    
    def test_regiments_reform_after_death(self):
        starting_ranks = 3
        self.assertEqual(starting_ranks, self.sut.formation_depth)

        self.sut.take_damage_front(
                damage=100000,
                target_count=self.sut.formation_width,
            )
        self.sut.resolve_unit_damage()

        self.assertEqual(starting_ranks - 1, self.sut.formation_depth)


if __name__ == '__main__':
    unittest.main()
