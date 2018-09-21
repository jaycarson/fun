#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Library import Library


class StatTest(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.sut = self.library.get_book('stat')

    def test_all_stat_flavors_are_balanced(self):
        for flavor in self.sut.stat_flavor_keys:
            total = 0

            for stat in self.sut.stat_flavors[flavor]:
                total += self.sut.stat_flavors[flavor][stat]

            error = flavor + "'s total is: " + str(total)
            self.assertEqual(12.0, total, error)

    def test_all_armor_flavors_are_balanced(self):
        for flavor in self.sut.armor_flavor_keys:
            pieces = self.sut.armor_flavors[flavor].keys()
            for piece in pieces:
                total = 0
                count = 0

                for stat in self.sut.armor_flavors[flavor][piece]:
                    total += self.sut.armor_flavors[flavor][piece][stat]
                    count += 1

                self.assertGreater(1.001, total/count)
                self.assertLess(0.999, total/count)


if __name__ == '__main__':
    unittest.main()
