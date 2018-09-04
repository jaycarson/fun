#!/usr/bin/python

from random import choice
from Components import Levelable
from Components import Skillable
from Components import RackArmor

from Character import Character, CharacterVPC, CharacterNPC, CharacterPC

from Library import BookStat


class Faction(object):
    def __init__(self,
                 experience=0,
                 race='human',
                 name='None',
                 faction_id=0,
                 clock=None,  # Clock Object
                 ):
        self.faction_id = faction_id
        self.locale_id = 0
        self.global_cooldown = 0
        self.races = ['human']
        self.book_stat = BookStat()

        self.skillable = Skillable()
        self.levelable = Levelable(
                    exp=experience,
                    skillable=self.skillable,
                )
        self.rack_armor = RackArmor()

        self.race = race
        self.name = name
        self.clock = clock

        self.weapons = {}

    def get_level(self):
        return self.levelable.get_level()

    def get_world_time(self):
        return self.clock.get_world_time()

    def give_weapon(self, weapon):
        weapon_id = weapon.get_id()
        self.weapons[weapon_id] = weapon

        return weapon_id

    def give_experience(self, experience):
        self.levelable.give_exp(experience)

    def get_experience(self):
        return self.levelable.exp

    def activate(self, dungeon_master, character):
        global_cooldown = 1000
        locale_time = character.get_locale_time()
        character.global_cooldown = locale_time + global_cooldown
        return character.global_cooldown

    def place_char(self, character, locations):
        looking = True
        
        while looking:
            location = choice(locations)
            if location.character is None:
                location.character = character
                character.location = location
                looking = False

    def create_vpc(self, name='any', race='any'):
        if race == 'any' or race not in self.races:
            race = choice(self.races)
        
        new_stats = self._book_stat.generate_for_character()
        
        new_character = CharacterVPC(
                experience=0,
                race=race,
                name=name,
                char_id=name,
                clock=self.clock,  # Clock Object
                stats=new_stats,  # Dictionary
            )

        self.vpcs.append(new_character)

        return new_character


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
