#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Clock import Clock
from Character import Character

from Smithy import SmithWeapon
from Smithy import SmithArmor

from Library import BookStat

from HexMap import HexMap


class DungeonMasterTest(unittest.TestCase):
    def setUp(self):
        self.locale_id = 5000
        self.start_time = 5
        self._clock = Clock()
        self._clock.add_locale(locale_id=self.locale_id, local_time=self.start_time)
        self._book_stat = BookStat()
        self.weapon_smith = SmithWeapon()
        self.arena = self.create_arena()

        npc_1 = self.create_npc()

        npc_2 = self.create_npc()


    def create_npc(self):
        new_stats = self._book_stat.generate_for_character()

        npc = Character(
            experience=0,
            race='human',
            name='Jon',
            char_id=0,
            clock=self._clock,
            stats=new_stats
            )
        npc.set_locale_id(self.locale_id)

        new_weapon = self.weapon_smith.create()
        npc.give_weapon(new_weapon)

        return npc

    def create_arena(self):
        hex_map = HexMap()
        hex_map.arena_ground = 'plains'
        hex_map.arena_height = 10
        hex_map.create_arena(radius=5)

        return hex_map

    def test_initial_world_time(self):
        test_time = 0
        self.assertEqual(test_time, self._clock.get_world_time())


if __name__ == '__main__':
    unittest.main()
