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
        self.gcd = 0

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
        self.dungeon_hex = None
        self.faction = None
        self.dm = None
        self.sight_range = 100
        self.max_health = 1000
        self.health = self.max_health
        self.movement = 3
        self.movement_speed = 1000

        self.traits = set()

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
        return self.faction.activate(self)

    def get_brain(self):
        combat_type = self.sets_weapon.get_active_combat_type()
        combat_role = self.sets_weapon.get_active_combat_role()

        return combat_type + combat_role

    def attack(self, slot=1, distance=1):
        weapon = self.get_weapon(slot)

        weapon.activate(
                self,
                slot,
                self.get_locale_time(),
                distance,
            )

    def attack_hyp(self, slot=1, distance=1):
        weapon = self.get_weapon(slot)

        if weapon is None:
            return -1

        return weapon.activate_hyp(
                actor=self,
                slot=slot,
                current_time=self.get_locale_time(),
                distance=distance,
            )

    def get_weapon(self, slot=1):
        ws = self.sets_weapon
        active_ws = self.get_active_weapon_set()

        if ws.active_weapon_set_both:
            weapon = ws.weapon_sets[active_ws]['both']
        elif slot <= 3:
            weapon = ws.weapon_sets[active_ws]['main']
        elif slot <= 5:
            weapon = ws.weapon_sets[active_ws]['off']

        return weapon

    def get_range(self, slot):
        return self.sets_weapon.get_active_slot_range(slot, self)

    def get_active_weapon_power(self, slot):
        weapon = self.get_weapon()
        return weapon.strengths[weapon.active_set][slot]

    def get_active_weapon_set(self):
        return self.sets_weapon.active_weapon_set

    def move(self, dungeon_hex):
        self.dungeon_hex.character = None
        self.dungeon_hex = dungeon_hex
        self.dungeon_hex.character = self

    def take_damage(self, damage, damage_type):
        self.health -= damage
        if self.health < 0:
            self.dm.remove_char(self)

    def take_gcd(self, cooldown):
        self.gcd = self.dm.get_time() + cooldown


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
