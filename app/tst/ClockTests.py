#!/usr/bin/python

import unittest
import sys
sys.path.insert(0, '../src')

from Clock import Clock


class ClockTest(unittest.TestCase):
    def setUp(self):
        self.sut = Clock()

    def test_initial_world_time(self):
        test_time = 0
        self.assertEqual(test_time, self.sut.get_world_time())

    def test_world_time_moves_forward(self):
        test_time =  1
        self.sut.increment_time()
        self.assertEqual(test_time, self.sut.get_world_time())

    def test_initial_default_locale_time(self):
        test_time = 0
        test_locale_id = 1
        self.sut.add_locale()
        self.assertEqual(
            test_time,
            self.sut.get_locale_time(locale_id=test_locale_id)
        )

    def test_initial_default_time_moves_forward(self):
        test_time = 1
        test_locale_id = 1
        self.sut.add_locale()
        self.sut.increment_locale_time(test_locale_id)
        self.assertEqual(
            test_time,
            self.sut.get_locale_time(locale_id=test_locale_id)
        )

    def test_set_locale_time(self):
        test_time = 0
        test_locale_id = 1000
        self.sut.add_locale(locale_id=test_locale_id)
        self.assertEqual(
            test_time,
            self.sut.get_locale_time(locale_id=test_locale_id)
        )

    def test_set_time_moves_forward(self):
        test_time = 1
        test_locale_id = 1000
        self.sut.add_locale(locale_id=test_locale_id)
        self.sut.increment_locale_time(test_locale_id)
        self.assertEqual(
            test_time,
            self.sut.get_locale_time(locale_id=test_locale_id)
        )

    def test_set_locale_time_with_time(self):
        test_time = 5000
        test_locale_id = 1000
        self.sut.add_locale(
            locale_id=test_locale_id,
            local_time=test_time
        )
        self.assertEqual(
            test_time,
            self.sut.get_locale_time(locale_id=test_locale_id)
        )

    def test_set_time_with_time_moves_forward(self):
        test_time_initial = 5000
        test_time = test_time_initial + 1
        test_locale_id = 1000
        self.sut.add_locale(
            locale_id=test_locale_id,
            local_time=test_time_initial
        )
        self.sut.increment_locale_time(test_locale_id)
        self.assertEqual(
            test_time,
            self.sut.get_locale_time(locale_id=test_locale_id)
        )


if __name__ == '__main__':
    unittest.main()
