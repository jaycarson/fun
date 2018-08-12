#!/usr/bin/python

from random import randint


class Clock(object):
    def __init__(self):
        self._clocks = {}  # local_id: time
        self._world_time = 0
        self._max_locale_id = 100000

    def set_world_time(self, world_time):
        self._world_time = time

    def set_local_time(self, locale_id, locale_time):
        self._clocks[locale_id] = locale_time

    def get_world_time(self):
        return self._world_time

    def get_locale_time(self, locale_id):
        return self._clocks.get(locale_id)

    def increment_time(self):
        self._world_time += 1

    def increment_locale_time(self, locale_id):
        self._clocks[locale_id] = self._clocks.get(locale_id) + 1

    def add_locale(self, locale_id=0, local_time=0):
        if locale_id == 0:
            locale_id = 1
            while locale_id in self._clocks.keys():
                locale_id = randint(0, self._max_locale_id)

        self._clocks[locale_id] = local_time

    def remove_locale(self, locale_id):
        assert locale_id in self._clocks.keys()
        del self._clocks[locale_id]
