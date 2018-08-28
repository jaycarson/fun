#!/usr/bin/python

from PriorityQueue import PriorityQueue


class DungeonMaster(object):
    def __init__(self, clock, dungeon, locale_id):
        self.clock = clock
        self.dungeon = dungeon
        self.locale_id = locale_id
        self.queue = PriorityQueue()
        self.teams = {}
        self.playing = True
        self.dungeon_expire = self.clock.max_locale_time

    def run_dungeon(self):
        while self.is_playing():
            self.run()

    def run(self):
        char = self.next_char()
        self.increment_time()
        while self.get_time() < char.global_cooldown:
            self.increment_time()
        self.activate_char(char)

    def is_playing(self):
        if self.get_time() > self.dungeon_expire:
            self.playing = False
        else:
            self.playing = True

        return self.playing

    def add_char(self, team_name, vpc):
        if team_name not in self.teams.keys():
            self.teams[team_name] = []

        self.teams[team_name].append(vpc)
        self.queue.put(vpc, self.get_time())

    def next_char(self):
        return self.queue.get()

    def get_time(self):
        return self.clock.get_locale_time(self.locale_id)

    def increment_time(self):
        self.clock.increment_locale_time(self.locale_id)

    def activate_char(self, char):
        self.queue.put(char, char.activate(self))
