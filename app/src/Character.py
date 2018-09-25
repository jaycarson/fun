#!/usr/bin/python

from Components import Levelable
from Components import Skillable
from Components import RackArmor
from Components import RackWeapon
from Components import SetsWeapon

from random import choice
from copy import deepcopy


class Character(object):
    def __init__(self,
                 library,  # The Library
                 experience=0,
                 race='human',
                 name='None',
                 char_id=0,
                 stats=None,  # Dictionary
                 ):
        self.char_id = char_id
        self.locale_id = 0
        self.gcd = 0
        self.library = library
        
        self.skillable = Skillable()
        self.levelable = Levelable(
                    exp=experience,
                    skillable=self.skillable,
                )

        self.sets_weapon = SetsWeapon()

        self.rack_armor = RackArmor(library=self.library)
        self.rack_weapon = RackWeapon(
                weapon_sets=self.sets_weapon,
                library=self.library,
            )

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

        self.hyp_set = 'active'

        self.traits = set()

        self.current_dungeon_master = None

        self.stats = stats

        self.target_enemy = None
        self.distance_to_enemy = 0
        
        self.target_ally = None
        self.distance_to_ally = 0
        self.moved = False

        self.buff_mult = 20
        self.status_count_zero = {
            'might': 0,
            'athletic': 0,
            'reflex': 0,
            'initiative': 0,
            'knowledge': 0,
            'reason': 0,
            'faith': 0,
            'perception': 0,
            'endurance': 0,
            'fortitude': 0,
            'presence': 0,
            'willpower': 0,
            'snare': 0,
            'chilled': 0,
            'vulnerability': 0,
        }

        self.status_count = deepcopy(self.status_count_zero)
        self.active_effects = []

        self.casting = False
        self.cast_time = 0

    def get_level(self):
        return self.levelable.get_level()

    def get_stat(self, stat):
        return self.stats.get(stat)

    def get_full_stat(self, stat):
        base_stat = self.stats.get(stat)
        armor_stat = self.rack_armor.get_stat(stat)
        weapon_stat = self.rack_weapon.get_stat(stat)
        buff_stat = self.status_count.get(stat) * self.buff_mult

        return base_stat + armor_stat + weapon_stat

    def get_locale_time(self):
        return self.get_time()

    def get_time(self):
        return self.dm.get_time()

    def get_power(self, slot):
        weapon = self.get_weapon()
        return weapon.strengths[weapon.active_set][slot]

    def get_cycle(self, slot):
        weapon = self.get_weapon()
        return weapon.cycles[weapon.active_set][slot]

    def get_cd_adj(self, slot):
        weapon = self.get_weapon()
        return weapon.cd_adjs[weapon.active_set][slot]

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

    def get_attack_dice(self):
        return self.get_dice_face_count('attack')

    def get_defense_dice(self):
        return self.get_dice_face_count('defense')

    def get_morale_dice(self):
        return self.get_dice_face_count('morale')

    def get_dice_face_count(self, face):
        count = 0
        count += self.rack_weapon.get_dice_for_face(face)
        count += self.rack_armor.get_dice_for_face(face)
        return count

    def attack(self, slot=1):
        weapon = self.get_weapon(slot)

        weapon.activate(self, slot)

    def attack_hyp(self, slot):
        weapon = self.get_weapon(slot)

        if weapon is None:
            return -1

        return weapon.activate_hyp(
                actor=self,
                slot=slot,
            )

    def get_weapon(self, slot=1):
        ws = self.sets_weapon
        active_ws = self.get_active_weapon_set()

        if ws.active_weapon_set_both:
            weapon = ws.weapon_sets[active_ws]['both']
        elif slot < 3:
            weapon = ws.weapon_sets[active_ws]['main']
        elif slot < 5:
            weapon = ws.weapon_sets[active_ws]['off']

        return weapon

    def get_range(self, slot):
        weapon = self.get_weapon()
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
        
        snare = self.status_count['snare'] * 100
        snare += self.status_count['chilled'] * 66
        move_speed = self.movement_speed + snare
        self.take_gcd(move_speed)

    def take_damage(self, damage, damage_type):
        self.health -= damage
        if self.health < 0:
            self.dm.remove_char(self)

    def take_gcd(self, cooldown):
        self.gcd = self.dm.get_time() + cooldown
    
    def roll_equipped_dice(self):
        self.rack_weapon.roll_dice()
        self.rack_armor.roll_dice()

    def receive_status_effects(self, status_effects):
        for effect in status_effects:
            effect.trigger(self)
            
            if effect.ticks > 1:
                self.active_effects.append(effect)

    def resolve_status_effects(self):
        self.status_count = deepcopy(self.status_count_zero)
        expired_effects = []

        for effect in self.active_effects:
            effect.tigger(self)
            if effect.ticks <= 1:
                expired_effects.append
            
        for expired_effect in expired_effects:
            self.active_effects.remove(expired_effect)


class CharacterPC(Character):
    def __init__(self,
                 library,
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
            library=library,
        )


class CharacterNPC(Character):
    def __init__(self,
                 library,
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
            library=library,
        )


class CharacterVPC(Character):
    def __init__(self,
                 library,
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
            library=library,
        )


class Regiment(Character):
    def __init__(self,
                 library,
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
            library=library,
        )
        return
