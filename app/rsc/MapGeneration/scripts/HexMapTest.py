#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from HexMap import HexMap


class DiceTest(unittest.TestCase):
    def setUp(self):
        self.sut = HexMap()
        self.sut.deserialize(path='../PNG/base_256_0001_.png')

    def test_getting_a_hex(self):
        test_hex = self.sut.get_hex(0, 0)
        test_r = test_hex.get_r()
        test_g = test_hex.get_g()
        test_b = test_hex.get_b()
        test_a = test_hex.get_a()
        self.assertEqual(255, test_r)
        self.assertEqual(129, test_g)
        self.assertEqual(129, test_b)
        self.assertEqual(129, test_a)

    def test_getting_neighbors_returns_the_right_quantity(self):
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.get_neighbors(test_hex)
        self.assertEqual(6, len(test_hexes))

    def test_getting_ring_returns_the_right_quantity_radius_1(self):
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.hex_ring(test_hex, 1)
        self.assertEqual(6, len(test_hexes))

    def test_getting_ring_returns_the_right_quantity_radius_2(self):
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.hex_ring(test_hex, 2)
        self.assertEqual(12, len(test_hexes))

    def test_getting_ring_returns_the_right_quantity_radius_3(self):
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.hex_ring(test_hex, 3)
        self.assertEqual(18, len(test_hexes))

    def test_getting_spiral_returns_the_right_quantity_radius_1(self):
        radius = 1
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.hex_spiral(test_hex, 1)
        count = 1
        ring_size = 0
        for ring in range(1, radius + 1):
            ring_size += 6
            count = count + ring_size
        self.assertEqual(count, len(test_hexes))

    def test_getting_spiral_returns_the_right_quantity_radius_2(self):
        radius = 2
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.hex_spiral(test_hex, 2)
        count = 1
        ring_size = 0
        for ring in range(1, radius + 1):
            ring_size += 6
            count = count + ring_size
        self.assertEqual(count, len(test_hexes))

    def test_getting_spiral_returns_the_right_quantity_radius_3(self):
        radius = 3
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.hex_spiral(test_hex, radius)
        count = 1
        ring_size = 0
        for ring in range(1, radius + 1):
            ring_size += 6
            count = count + ring_size
        self.assertEqual(count, len(test_hexes))

    def test_getting_spiral_returns_the_right_quantity_radius_15(self):
        radius = 15
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.hex_spiral(test_hex, radius)
        count = 1
        ring_size = 0
        for ring in range(1, radius + 1):
            ring_size += 6
            count = count + ring_size
        self.assertEqual(count, len(test_hexes))

    def test_getting_spiral_returns_the_right_quantity_radius_40(self):
        radius = 40
        test_hex = self.sut.get_hex(0, 0)
        test_hexes = self.sut.hex_spiral(test_hex, radius)
        count = 1
        ring_size = 0
        for ring in range(1, radius + 1):
            ring_size += 6
            count = count + ring_size
        self.assertEqual(count, len(test_hexes))


if __name__ == '__main__':
    unittest.main()
