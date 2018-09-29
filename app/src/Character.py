#!/usr/bin/python

from Components import Levelable
from Components import Skillable
from Components import RackArmor
from Components import RackWeapon
from Components import SetsWeapon

from random import choice
from copy import deepcopy


class Unit(object):
    def __init__(self,
                 library,  # The Library
                 stats,
                 experience=0,
                 race='human',
                 name='None',
                 char_id=0,
                 ):
        self.char_id = char_id
        self.locale_id = 0
        self.gcd = 0
        self.combat_mode = 'skirmish'  # skirmish/battle
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
        self.turn_cost = 0.25

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
        
        self.facing = 0  # 0 = North. 0-5 Clockwise
        self.formation_width = 1
        self.formation_depth = 1

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

    def get_direction_to_unit(self, target):
        return dm.direction_to_unit(source=self, target=target)

    def get_side_to_unit(self, target):
        direction = self.get_direction_to_unit(target)
        side = direction - self.facing

        if side < 0:
            side += 6
        if side > 5:
            side -= 6

        return side

    def get_attack_count(self, side):
        if side == 4 or side == 2:
            attack_count = self.formation_depth
        else:
            attack_count = self.formation_width

    def move(self, dungeon_hex):
        self.dungeon_hex.character = None
        self.dungeon_hex = dungeon_hex
        self.dungeon_hex.character = self
        
        snare = self.status_count['snare'] * 100
        snare += self.status_count['chilled'] * 66
        move_speed = self.movement_speed + snare
        self.take_gcd(move_speed)

    def take_damage(self, damage, damage_type, target_count=1, side=0):
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


class Character(Unit):
    def __init__(self,
                 library,  # The Library
                 stats,  # Dictionary
                 experience=0,
                 race='human',
                 name='None',
                 char_id=0,
                 ):
        Unit.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
            char_id=char_id,
            stats=stats,
            library=library,
        )


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
        self.size = 1
        self.max_size = 30
        self.soldiers = [Soldier(self.max_health)]

    def add_unit(self, quanitity=1):
        self.size += quantity
        count = len(self.soldiers)

        if count + quanitity > self.max_size:
            quantity = self.max_size - count

        for new_soldier in range(0, quantity):
            self.soldiers.append(Soldier(self.max_health))
    
    def get_laps(self, target_count):
        return min(target_count / len(self.soldiers), 3)

    def take_damage(self, damage, damage_type, target_count=1, side=0):
        # TODO damage modification based on resistances

        if side == 2:
            self.take_damage_right_side(damage, target_count)
        elif side == 4:
            self.take_damage_left_side(damage, target_count)
        elif side == 3:
            self.take_damage_rear(damage, target_count)
        else:
            self.take_damage_front(damage, target_count)

        self.resolve_unit_damage()

    def take_damage_front(self, damage, target_count):
        for lap in range(0, self.get_laps(target_count) + 1):
            for target in range(0, target_count):
                soldiers[target].take_damage(damage)

    def take_damage_left_side(self, damage, target_count):
        laps = target_count / len(self.soldiers)

        for lap in range(0, self.get_laps(target_count) + 1):
            for row in range(0, self.formation_width):
                for column in range(0, self.formation_depth):
                    target = row * self.formation_width + column

                    if target <= len(self.soldiers):
                        soldiers[target].take_damage(damage)
                        target_count -= 1
                        if target_count <= 0:
                            return

    def take_damage_right_side(self, damage, target_count):
        laps = target_count / len(self.soldiers)

        for lap in range(0, self.get_laps(target_count) + 1):
            for row in range(self.formation_width, 0):
                for column in range(0, self.formation_depth):
                    target = row * self.formation_width + column

                    if target <= len(self.soldiers):
                        soldiers[target].take_damage(damage)
                        target_count -= 1
                        if target_count <= 0:
                            return

    def take_damage_rear(self, damage, target_count):
        laps = target_count / len(self.soldiers)

        for lap in range(0, self.get_laps(target_count) + 1):
            for target in range(target_count, 0):
                soldiers[target].take_damage(damage)

    def resolve_unit_damage(self):
        for soldier in soldiers:
            if soldier.health <= 0:
                soldiers.remove(soldier)

        self.formation_depth = len(soldiers) / self.formation_width


class Soldier(object):
    def __init__(self, health):
        self.health = health
        self.max_health = health

    def take_damage(self, damage):
        self.health = max(self.health - damage, 0)

    def heal_damage(self, heal):
        self.health = min(self.health + heal, self.max_health)
