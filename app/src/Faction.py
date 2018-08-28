#!/usr/bin/python

from Library import BookArmor
from random import choice


class Faction(object):
    def __init__(self,
                 experience=0,
                 race='human',
                 name='None',
                 char_id=0,
                 clock=None,  # Clock Object
                 stats=None,  # Dictionary
                 ):
        self.experience = experience
        self.char_id = char_id
        self.locale_id = 0
        self.global_cooldown = 0

        self.race = race
        self.name = name
        self.clock = clock

        self.weapons = {}
        self.armors = {}

        self.skills = []
        self.skill_points_current = 0
        self.skill_points_total = 0

        self.armors_by_piece = {}

    def get_level(self):
        level = self.experience / 1000

        if level > 40:
            level = 40

        return level

    def get_world_time(self):
        return self.clock.get_world_time()

    def get_locale_time(self):
        return self.clock.get_locale_time(self.locale_id)

    def _gain_level(self):
        self._gain_skill_point()

    def _gain_skill_point(self):
        self.skill_points_current += 1
        self.skill_points_total += 1

    def give_weapon(self, weapon):
        weapon_id = weapon.get_id()
        self.weapons[weapon_id] = weapon

        return weapon_id

    def give_armor(self, armor):
        armor_id = armor.get_id()
        self.armors[armor.get_id()] = armor

        piece = armor.get_piece()
        self.armors_by_piece[piece][armor_id] = armor

        return armor_id

    def give_experience(self, experience):
        starting_level = self.get_level()

        self.experience += experience

        current_level = self.get_level()

        if current_level > starting_level:
            levels_gained = current_level - starting_level
            for x in range(0, levels_gained):
                self._gain_level()

    def activate(self, dungeon_master, character):
        global_cooldown = 1000
        character.global_cooldown = self.get_locale_time() + global_cooldown
        return characater.global_cooldown

    def place_char(self, character, locations):
        looking = True
        
        while looking:
            location = choice(locations)
            if location.character is None:
                location.character = character
                character.location = location
                looking = False


class FactionPC(Faction):
    def __init__(self, experience=0, race='human', name='None'):
        Faction.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
        )


class FactionNPC(Faction):
    def __init__(self, experience=0, race='human', name='None'):
        Faction.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
        )


class FactionVPC(Faction):
    def __init__(self, experience=0, race='human', name='None'):
        Faction.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
        )
