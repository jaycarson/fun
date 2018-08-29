#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from DungeonMaster import DungeonMaster

from Clock import Clock
from Character import Character
from Faction import Faction

from Smithy import SmithWeapon
from Smithy import SmithArmor

from Library import BookStat

from HexMap import HexMap


class DungeonMasterTest(unittest.TestCase):
    def setUp(self):
        self.locale_id = 5000
        self.start_time = 1

        self.sut = DungeonMaster(
                clock=Clock(),
                dungeon=self.create_arena(),
                locale_id=self.locale_id,
            )

        self.sut.clock.add_locale(
                locale_id=self.locale_id,
                local_time=self.start_time,
            )

        self._book_stat = BookStat()
        self.weapon_smith = SmithWeapon()

    def create_vpc(self, name):
        new_stats = self._book_stat.generate_for_character()

        npc = Character(
            experience=0,
            race='human',
            name=name,
            char_id=0,
            clock=self.sut.clock,
            stats=new_stats
            )
        npc.locale_id = self.locale_id

        new_weapon = self.weapon_smith.create()
        npc.give_weapon(new_weapon)

        return npc

    def create_faction(self, name):
        return Faction(
            experience=0,
            race='human',
            name=name,
            faction_id=name,
            clock=self.sut.clock,
            )

    def create_arena(self):
        hex_map = HexMap()
        hex_map.arena_ground = 'plains'
        hex_map.arena_height = 10
        hex_map.create_arena(radius=5)

        return hex_map

    def add_chars_to_dungeon(self):
        self.vpc_1 = self.create_vpc('jon')
        self.vpc_2 = self.create_vpc('joe')
        self.faction_1 = self.create_faction('red')
        self.faction_2 = self.create_faction('blue')
        self.vpc_1.faction = self.faction_1
        self.vpc_2.faction = self.faction_2
        self.chars = [self.vpc_1, self.vpc_2]

        self.sut.add_char(faction=self.faction_1, member=self.vpc_1, edge='ne')
        self.sut.add_char(faction=self.faction_2, member=self.vpc_2, edge='sw')

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
        
        self.assertGreaterEqual(abs(test_char.location.x), 0)
        self.assertGreaterEqual(abs(test_char.location.y), 0)
        self.assertGreaterEqual(abs(test_char.location.z), 0)

        self.assertGreaterEqual(radius, abs(test_char.location.x))
        self.assertGreaterEqual(radius, abs(test_char.location.y))
        self.assertGreaterEqual(radius, abs(test_char.location.z))



if __name__ == '__main__':
    unittest.main()
