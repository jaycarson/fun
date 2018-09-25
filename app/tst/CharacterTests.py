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


class CharacterTest(unittest.TestCase):
    def setUp(self):
        self._clock = Clock()
        self.locale_id = 1000
        self.library = Library()
        self.book_stat = self.library.get_book('stat')
        self.sut_smithy = Smithy()
        self.sut_brains = Brains()

        self.sut_faction = Faction(
                    experience=0,
                    name='Red',
                    faction_id='1000',
                    clock=self._clock,
                    smithy_weapon=self.sut_smithy,
                    brains=self.sut_brains,
                    library=self.library
                )

        self.sut = self.sut_faction.create_vpc(name='sut')

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

        self.sut_dm.add_char(
                member=self.sut,
                faction=self.sut_faction,
                edge='sw',
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
        sut_1 = Character(char_id=expected_1, library=self.library)
        sut_2 = Character(char_id=expected_2, library=self.library)
        self.assertEqual(expected_1, sut_1.char_id)
        self.assertEqual(expected_2, sut_2.char_id)

    def test_gets_name(self):
        expected = 'sut'
        self.assertEqual(expected, self.sut.name)

    def test_character_knows_the_worlds_time(self):
        test_time = 0
        self.assertEqual(test_time, self.sut.faction.get_world_time())
        self._clock.increment_time()

    def test_character_still_knows_the_worlds_time(self):
        test_time = 1
        self._clock.increment_time()
        self.assertEqual(test_time, self.sut.faction.get_world_time())

    def test_character_knows_the_locale_time(self):
        test_locale_id = 1
        test_time = 0
        self._clock.add_locale(locale_id=test_locale_id)
        self.sut.locale_id = test_locale_id
        self.assertEqual(test_time, self.sut.dm.get_time())

    def test_character_still_knows_the_locale_time(self):
        test_locale_id = 1
        test_time = 1
        self.sut.dm.increment_time()
        self.assertEqual(test_time, self.sut.dm.get_time())

    def test_character_has_stats(self):
        base_stat = self.book_stat.get_base_stat()
        stat_list = self.book_stat.get_list()

        for stat in stat_list:
            self.assertEqual(base_stat, self.sut.get_stat(stat))

    def test_character_gets_a_weapon(self):
        weapon_smith = SmithWeapon(library=self.library)
        new_weapon = weapon_smith.create()
        weapon_id = self.sut.rack_weapon.give_weapon(new_weapon)
        self.sut.sets_weapon.equip_weapon_by_id(weapon_id=weapon_id)
        equipped_weapon = self.sut.sets_weapon.get_equipped_weapon()
        self.assertEqual(equipped_weapon, new_weapon)

    def test_character_gets_a_weapon_and_automatically_equips_it(self):
        self.sut.sets_weapon.weapon_sets[1]['main'] = None
        self.sut.sets_weapon.weapon_sets[1]['off'] = None
        self.sut.sets_weapon.weapon_sets[1]['both'] = None
        weapon_smith = SmithWeapon(library=self.library)
        new_weapon = weapon_smith.create()
        self.sut.rack_weapon.give_weapon(new_weapon)
        equipped_weapon = self.sut.sets_weapon.get_equipped_weapon()
        self.assertEqual(equipped_weapon, new_weapon)

    def test_character_gets_an_armor_and_automatically_equips_it(self):
        armor_smith = SmithArmor(library=self.library)
        for piece in armor_smith.armor_pieces:
            self.sut.rack_armor.remove_armor(piece)
        new_armor = armor_smith.create()
        piece = new_armor.piece
        self.sut.rack_armor.give_armor(new_armor)
        equipped_armor = self.sut.rack_armor.get_equipped_armor(piece)
        self.assertEqual(equipped_armor, new_armor)


class CharacterCombatTest(unittest.TestCase):
    def setUp(self):
        self._clock = Clock()
        self.library = Library()
        self.locale_id = 1000
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
                    library=self.library,
                )

        self.sut2_faction = Faction(
                    experience=0,
                    name='blue',
                    faction_id='1001',
                    clock=self._clock,
                    smithy_weapon=self.sut_smithy_weapon,
                    smithy_armor=self.sut_smithy_armor,
                    brains=self.sut_brains,
                    library=self.library,
                )

        self.sut = self.sut_faction.create_vpc(name='sut')
        self.sut2 = self.sut2_faction.create_vpc(name='sut2')

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

        self.sut_dm.add_char(
                member=self.sut,
                faction=self.sut_faction,
                edge='sw',
            )

        self.sut_dm.add_char(
                member=self.sut2,
                faction=self.sut2_faction,
                edge='se',
            )

        weapon_smith = SmithWeapon(library=self.library)
        new_weapon = weapon_smith.create()
        self.sut.rack_weapon.give_weapon(new_weapon)

    def test_weapon_starts_off_cooldown(self):
        weapon = self.sut.sets_weapon.get_equipped_weapon()
        slot = 2
        self.sut.dm.increment_time()
        locale_time = self.sut.dm.get_time()
        self.assertFalse(weapon.on_cooldown(slot, locale_time))

    def test_weapon_goes_on_cooldown(self):
        weapon = self.sut.sets_weapon.get_equipped_weapon()
        slot = 2
        self.sut.dm.increment_time()
        self.sut.target_enemy = self.sut2
        self.sut.attack(slot)
        locale_time = self.sut.dm.get_time()
        self.assertTrue(weapon.on_cooldown(slot, locale_time))


if __name__ == '__main__':
    unittest.main()
