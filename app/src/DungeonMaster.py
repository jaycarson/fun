#!/usr/bin/python

from PriorityQueue import PriorityQueue
from PathFinder import PathFinder


class DungeonMaster(object):
    def __init__(self, clock, dungeon, locale_id, library):
        self.library = library
        self.clock = clock
        self.dungeon = dungeon
        self.path_finder = PathFinder(dungeon)
        self.locale_id = locale_id
        self.queue = PriorityQueue()
        self.factions = {}
        self.playing = True
        self.dungeon_expire = self.clock.max_locale_time
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

        self.clock.set_local_time(locale_id=locale_id, locale_time=0)

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
        while self.get_time() < char.gcd:
            self.increment_time()
        self.activate_char(char)

    def is_playing(self):
        if self.get_time() > self.dungeon_expire:
            self.playing = False
        elif len(self.factions) <= 1:
            self.playing = False
        else:
            self.playing = True

        return self.playing

    def add_char(self, member, faction='dm', edge='dm', insert_time=0):
        if faction == 'dm':
            faction = self

        if faction.faction_id not in self.factions.keys():
            self.factions[faction.faction_id] = []

        if insert_time == 0:
            insert_time = self.get_time() + member.get_stat('initiative')

        self.factions[faction.faction_id].append(member)
        self.queue.put(member, insert_time)

        member.dm = self

        faction.place_char(member, self.get_placement_locations(edge))
        member.roll_equipped_dice()

    def remove_char(self, member):
        faction_id = member.faction.faction_id
        self.factions[faction_id].remove(member)
        if len(self.factions[faction_id]) == 0:
            self.factions.pop(faction_id, None)

    def next_char(self):
        return self.queue.get()

    def get_time(self):
        return self.clock.get_locale_time(self.locale_id)

    def increment_time(self):
        self.clock.increment_locale_time(self.locale_id)

    def activate_char(self, char):
        priority = char.activate()

        if char.health > 0:
            self.queue.put(char, priority)

    def get_placement_locations(self, edge):
        sides = ['ne', 'e', 'se', 'sw', 'w', 'nw']

        if edge in sides:
            return self.placement_locations[edge]

    def get_adjacent_enemies(self, requestor):
        hexes = self.dungeon.neighbors(requestor.dungeon_hex)
        return self.get_enemies(requestor, hexes)

    def get_enemies_in_line(self, requestor, direction, distance):
        hexes = self.dungeon.line(requestor.dungeon_hex, direction, distance)
        return self.get_enemies(requestor, hexes)

    def get_nearby_enemies(self, requestor, radius=2):
        hexes = self.dungeon.spiral(requestor.dungeon_hex, radius)
        return self.get_enemies(requestor, hexes)

    def get_enemies(self, requestor, hexes):
        enemies = []

        for dungeon_hex in hexes:
            if dungeon_hex is None:
                next
            elif dungeon_hex.character is None:
                next
            elif dungeon_hex.character.faction != requestor.faction:
                enemies.append(dungeon_hex.character)

        return enemies

    def get_nearest_enemy(self, requestor):
        enemies = []
        min_dist = requestor.sight_range
        closest = None

        for faction in self.factions.keys():
            if faction != requestor.faction.faction_id:
                for member in self.factions[faction]:
                    enemies.append(member)

        for enemy in enemies:
            current = self.distance(requestor, enemy)
            if current < min_dist:
                min_dist = current
                closest = enemy

        requestor.target_enemy = enemy
        requestor.distance_to_enemy = min_dist

        return closest

    def get_neighboring_hex(self, actor, direction):
        return self.dungeon.neighbor(actor.dungeon_hex, direction)

    def is_neighboring_hex_empty(self, actor, direction):
        neighbor = self.get_neighboring_hex(actor, direction)
        if neighbor.character is None:
            return True
        else:
            return False

    def distance(self, actor, target):
        return self.dungeon.distance(actor.dungeon_hex, target.dungeon_hex)

    def move_char_along_path(self, actor, source, dest, distance):
        path = self.path_finder.find_path(
                start=source,
                goal=dest,
            )
        if (len(path) - 1) < distance:
            distance = (len(path) - 1)
        actor.move(path[distance])

