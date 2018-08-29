#!/usr/bin/python

from PriorityQueue import PriorityQueue


class DungeonMaster(object):
    def __init__(self, clock, dungeon, locale_id):
        self.clock = clock
        self.dungeon = dungeon
        self.locale_id = locale_id
        self.queue = PriorityQueue()
        self.factions = {}
        self.playing = True
        self.dungeon_expire = self.clock.max_locale_time
        self.factions = {}
        self.char_id = 'DM'
        self.placement_locations = {
                'ne': [],    
                'e': [],    
                'se': [],    
                'nw': [],    
                'w': [],    
                'sw': [],    
            }
        self.init_placement_locations()

    def init_placement_locations(self):
        center = self.dungeon.get_hex(x=0, y=0, z=0)
        ring_1 = self.dungeon.ring(center, self.dungeon.map_radius-1)
        ring_2 = self.dungeon.ring(center, self.dungeon.map_radius)
        rings = ring_1 + ring_2

        high = self.dungeon.map_radius - 1
        low = 1

        for point in rings:
            x = abs(point.x)
            y = abs(point.y)
            z = abs(point.z)

            if x >= high and y > low and y < high:
                if point.x < 0:
                    self.placement_locations['w'].append(point)
                else:
                    self.placement_locations['e'].append(point)
            elif y >= high and x > low and x < high:
                if point.y < 0:
                    self.placement_locations['se'].append(point)
                else:
                    self.placement_locations['nw'].append(point)
            elif z >= high and x > low and x < high:
                if point.z < 0:
                    self.placement_locations['ne'].append(point)
                else:
                    self.placement_locations['sw'].append(point)

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

    def add_char(self, member, faction='dm', edge='dm'):
        if faction == 'dm':
            faction = self

        if faction.faction_id not in self.factions.keys():
            self.factions[faction.faction_id] = []

        self.factions[faction.faction_id].append(member)
        self.queue.put(member, self.get_time())

        faction.place_char(member, self.get_placement_locations(edge))

    def next_char(self):
        return self.queue.get()

    def get_time(self):
        return self.clock.get_locale_time(self.locale_id)

    def increment_time(self):
        self.clock.increment_locale_time(self.locale_id)

    def activate_char(self, char):
        priority = char.faction.activate(self, char)
        
        self.queue.put(char, priority)

    def get_placement_locations(self, edge):
        sides = ['ne', 'e', 'se', 'sw', 'w', 'nw']

        if edge in sides:
            return self.placement_locations[edge]
