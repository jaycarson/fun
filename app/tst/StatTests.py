#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Library import Library


class StatTest(unittest.TestCase):
    def setUp(self):
        library = Library()
        self.sut = library.get_book('stat')

    def test_all_stat_flavors_are_balanced(self):
        for flavor in self.sut.stat_flavor_keys:
            total = 0

            for stat in self.sut.stat_flavors[flavor]:
                total += self.sut.stat_flavors[flavor][stat]

            error = flavor + "'s total is: " + str(total)
            self.assertEqual(12.0, total, error)


if __name__ == '__main__':
    unittest.main()
