#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from DungeonMaster import DungeonMaster

from Clock import Clock
from Character import Character
from Faction import Faction

from Smithy import Smithy

from Library import Library

from HexMap import HexMap

from Brain import Brains


class DungeonMasterTest(unittest.TestCase):
    def setUp(self):
        self.locale_id = 5000
        self.start_time = 1
        self.library = Library()

        self.sut = DungeonMaster(
                clock=Clock(),
                dungeon=self.create_arena(),
                locale_id=self.locale_id,
                library=self.library
            )

        self.sut.clock.add_locale(
                locale_id=self.locale_id,
                local_time=self.start_time,
            )

        self._book_stat = self.library.get_book('stat')
        self.smithy = Smithy(library=self.library)
        self.smith_weapon = self.smithy.get_smith('weapon')
        self.smith_armor = self.smithy.get_smith('armor')
        self.brains = Brains()

    def create_vpc(self, name):
        new_stats = self._book_stat.generate_for_character()

        npc = Character(
            experience=0,
            race='human',
            name=name,
            char_id=0,
            clock=self.sut.clock,
            stats=new_stats,
            library=self.library,
            )
        npc.locale_id = self.locale_id

        new_weapon = self.weapon_smith.create()
        npc.rack_weapon.give_weapon(new_weapon)

        return npc

    def create_faction(self, name):
        return Faction(
            experience=0,
            name=name,
            faction_id=name,
            clock=self.sut.clock,
            smithy=self.smithy,
            brains=self.brains,
            library=self.library,
            )

    def create_arena(self):
        hex_map = HexMap()
        hex_map.arena_ground = 'plains'
        hex_map.arena_height = 10
        hex_map.create_arena(radius=5)

        return hex_map

    def add_chars_to_dungeon(self):
        self.faction_1 = self.create_faction('red')
        self.faction_2 = self.create_faction('blue')
        self.vpc_1 = self.faction_1.create_vpc(name='jon')
        self.vpc_2 = self.faction_2.create_vpc(name='joe')
        self.chars = [self.vpc_1, self.vpc_2]

        self.sut.add_char(
                faction=self.faction_1,
                member=self.vpc_1,
                edge='ne',
                insert_time=0,
            )
        self.sut.add_char(
                faction=self.faction_2,
                member=self.vpc_2,
                edge='sw',
                insert_time=1,
            )

    def test_initial_world_time(self):
        test_time = 0
        self.assertEqual(test_time, self.sut.clock.get_world_time())

    def test_dungeon_master_accepts_vpcs(self):
        self.add_chars_to_dungeon()
        self.assertTrue(self.sut.next_char() in self.chars)

    def test_run_dungeon_for_a_few_rounds(self):
        self.add_chars_to_dungeon()
        start_time = self.sut.get_time()
        self.sut.run()
        self.sut.run()
        self.sut.run()
        end_time = self.sut.get_time()
        self.assertGreater(end_time, start_time)

    def test_run_dungeon_for_the_entire_game(self):
        self.add_chars_to_dungeon()
        start_time = self.sut.get_time()
        self.sut.run_dungeon()
        end_time = self.sut.get_time()
        self.assertGreater(end_time, start_time)

    def test_characters_got_placed(self):
        self.add_chars_to_dungeon()
        test_char = self.sut.next_char()
        radius = self.sut.dungeon.map_radius
        
        self.assertGreaterEqual(abs(test_char.dungeon_hex.x), 0)
        self.assertGreaterEqual(abs(test_char.dungeon_hex.y), 0)
        self.assertGreaterEqual(abs(test_char.dungeon_hex.z), 0)

        self.assertGreaterEqual(radius, abs(test_char.dungeon_hex.x))
        self.assertGreaterEqual(radius, abs(test_char.dungeon_hex.y))
        self.assertGreaterEqual(radius, abs(test_char.dungeon_hex.z))


if __name__ == '__main__':
    unittest.main()
