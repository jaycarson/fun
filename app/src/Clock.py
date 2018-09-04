#!/usr/bin/python

from random import randint


class Clock(object):
    def __init__(self):
        self.clocks = {}  # local_id: time
        self.world_time = 0
        self.max_locale_time = 100000

    def set_world_time(self, world_time):
        self.world_time = time

    def set_local_time(self, locale_id, locale_time):
        self.clocks[locale_id] = locale_time

    def get_world_time(self):
        return self.world_time

    def get_locale_time(self, locale_id):
        assert locale_id in self.clocks.keys()
        return self.clocks.get(locale_id)

    def increment_time(self):
        self.world_time += 1

    def increment_locale_time(self, locale_id):
        self.clocks[locale_id] = self.clocks.get(locale_id) + 1

    def add_locale(self, locale_id=0, local_time=0):
        if locale_id == 0:
            locale_id = 1
            while locale_id in self.clocks.keys():
                locale_id = randint(0, self.max_locale_time)

        self.clocks[locale_id] = local_time

    def remove_locale(self, locale_id):
        assert locale_id in self.clocks.keys()
        del self.clocks[locale_id]
