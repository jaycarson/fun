#!/usr/bin/python

from random import choice
from Components import Levelable
from Components import Skillable
from Components import RackArmor
from Components import RackWeapon
from Components import SetsWeapon


class Character(object):
    def __init__(self,
                 experience=0,
                 race='human',
                 name='None',
                 char_id=0,
                 stats=None,  # Dictionary
                 ):
        self.char_id = char_id
        self.locale_id = 0
        self.global_cooldown = 0

        self.skillable = Skillable()
        self.levelable = Levelable(
                    exp=experience,
                    skillable=self.skillable,
                )
        
        self.sets_weapon = SetsWeapon()
        
        self.rack_armor = RackArmor()
        self.rack_weapon = RackWeapon(self.sets_weapon)
        
        self.sets_weapon.rack_weapon = self.rack_weapon

        self.race = race
        self.name = name
        self.local_id = 0
        self.location = None
        self.faction = None
        self.dm = None

        self.current_dungeon_master = None

        self.stats = stats

        self.target_enemy = None
        self.target_ally = None

    def get_level(self):
        return self.levelable.get_level()

    def get_stat(self, stat):
        return self.stats.get(stat)

    def get_locale_time(self):
        return self.dm.get_time()

    def give_experience(self, experience):
        self.levelable.give_exp(experience)
    
    def get_experience(self):
        return self.levelable.exp

    def activate(self):
        self.faction.activate(self)

    def attack(self, slot=1):
        ws = self.sets_weapon
        active_ws = self.sets_weapon.active_weapon_set

        if ws.active_weapon_set_both:
            attack_set = ws.weapon_sets[active_ws]['both']
        elif slot <= 3:
            attack_set = ws.weapon_sets[active_ws]['main']
        elif slot <= 5:
            attack_set = ws.weapon_sets[active_ws]['off']
        
        attack_set.activate(
                self,
                slot,
                self.get_locale_time(),
            )

    def move(self, location):
        self.location.character = None
        self.location = location
        self.location.character = self


class CharacterPC(Character):
    def __init__(self,
                 experience=0,
                 race='human',
                 name='None',
                 char_id=0,
                 stats=None,  # Dictionary
                 ):
        Character.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
            char_id=char_id,
            stats=stats,
        )


class CharacterNPC(Character):
    def __init__(self,
                 experience=0,
                 race='human',
                 name='None',
                 char_id=0,
                 stats=None,  # Dictionary
                 ):
        Character.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
            char_id=char_id,
            stats=stats,
        )


class CharacterVPC(Character):
    def __init__(self,
                 experience=0,
                 race='human',
                 name='None',
                 char_id=0,
                 stats=None,  # Dictionary
                 ):
        Character.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
            char_id=char_id,
            stats=stats,
        )
