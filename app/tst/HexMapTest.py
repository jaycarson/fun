#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from HexMap import HexMap


class HexMapTest(unittest.TestCase):
    def setUp(self):
        self.sut = HexMap()
        self.sut.deserialize(path='../rsc/MapGeneration/PNG/noise_h_map_solid_256_4_1_2675506463.png')

    def test_getting_a_hex(self):
        test_hex = self.sut.get_hex(0, 0)
        self.assertEqual(126, test_hex.r)
        self.assertEqual(126, test_hex.g)
        self.assertEqual(126, test_hex.b)
        self.assertEqual(255, test_hex.a)

    def test_getting_neighbors_returns_the_right_quantity(self):
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.neighbors(test_hex)
        self.assertEqual(6, len(test_hexes))

    def test_getting_ring_returns_the_right_quantity_radius_1(self):
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.ring(test_hex, 1)
        self.assertEqual(6, len(test_hexes))

    def test_getting_ring_returns_the_right_quantity_radius_2(self):
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.ring(test_hex, 2)
        self.assertEqual(12, len(test_hexes))

    def test_getting_ring_returns_the_right_quantity_radius_3(self):
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.ring(test_hex, 3)
        self.assertEqual(18, len(test_hexes))

    def test_getting_spiral_returns_the_right_quantity_radius_1(self):
        radius = 1
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.spiral(test_hex, 1)
        count = 1
        ring_size = 0
        for ring in range(1, radius + 1):
            ring_size += 6
            count = count + ring_size
        self.assertEqual(count, len(test_hexes))

    def test_getting_spiral_returns_the_right_quantity_radius_2(self):
        radius = 2
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.spiral(test_hex, 2)
        count = 1
        ring_size = 0
        for ring in range(1, radius + 1):
            ring_size += 6
            count = count + ring_size
        self.assertEqual(count, len(test_hexes))

    def test_getting_spiral_returns_the_right_quantity_radius_3(self):
        radius = 3
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.spiral(test_hex, radius)
        count = 1
        ring_size = 0
        for ring in range(1, radius + 1):
            ring_size += 6
            count = count + ring_size
        self.assertEqual(count, len(test_hexes))

    def test_getting_spiral_returns_the_right_quantity_radius_15(self):
        radius = 15
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.spiral(test_hex, radius)
        count = 1
        ring_size = 0
        for ring in range(1, radius + 1):
            ring_size += 6
            count = count + ring_size
        self.assertEqual(count, len(test_hexes))

    def test_getting_spiral_returns_the_right_quantity_radius_40(self):
        radius = 40
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.spiral(test_hex, radius)
        count = 1
        ring_size = 0
        for ring in range(1, radius + 1):
            ring_size += 6
            count = count + ring_size
        self.assertEqual(count, len(test_hexes))


class HexMapArenaTest(unittest.TestCase):
    def setUp(self):
        self.sut = HexMap()
        self.radius = 5
        self.arena_ground = 'plains'
        self.arena_height = 10
        self.sut.arena_ground = self.arena_ground
        self.sut.arena_height = self.arena_height
        self.sut.create_arena(radius=self.radius)

    def test_getting_a_hex(self):
        test_hex = self.sut.get_hex(0, 0)
        self.assertEqual(self.arena_height, test_hex.height)

    def test_getting_another_hex(self):
        test_hex = self.sut.get_hex(5, 0, -5)
        self.assertEqual(self.arena_height, test_hex.height)


if __name__ == '__main__':
    unittest.main()
