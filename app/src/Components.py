#!/usr/bin/python

from Library import BookArmor


class Levelable(object):
    def __init__(self,
                 skillable=None,
                 exp=0,
                 ):
        self.exp = exp
        self.skillable = skillable

        if skillable is None:
            self.give_exp = self.give_exp_without_skill
        else:
            self.give_exp = self.give_exp_with_skill

    def get_level(self):
        level = self.exp / 1000

        if level > 40:
            level = 40

        return level
    
    def give_exp_without_skill(self, exp):
        self.exp += exp

    def give_exp_with_skill(self, exp):
        starting_level = self.get_level()

        self.exp += exp

        current_level = self.get_level()

        if current_level > starting_level:
            levels_gained = current_level - starting_level
            for x in range(0, levels_gained):
                self.skillable.gain_level()


class Skillable(object):
    def __init__(self):
        self.skill_points_current = 0
        self.skill_points_total = 0

    def gain_level(self):
        self.skill_points_current += 1
        self.skill_points_total += 1


class RackArmor(object):
    def __init__(self):
        self.armors = {}
        self.armors_by_piece = {}
        self.armors_equiped_by_piece = {}

        for piece in BookArmor().get_pieces():
            self.armors_by_piece[piece] = {}
            self.armors_equiped_by_piece[piece] = None

    def give_armor(self, armor):
        self.armors[armor.id] = armor

        self.armors_by_piece[armor.piece][armor.id] = armor

        if self.get_equiped_armor(armor.piece) is None:
            self.equip_armor(armor)

        return armor.id

    def equip_armor(self, armor):
        self.armors_equiped_by_piece[armor.piece] = armor

    def get_equiped_armor(self, piece='chest'):
        return self.armors_equiped_by_piece[piece]


class RackWeapon(object):
    def __init__(self, weapon_sets=None):
        self.weapons = {}

        if weapon_sets is None:
            self.give_weapon = self.give_weapon_not_equipable
        else:
            self.sets_weapon = weapon_sets
            self.give_weapon = self.give_weapon_equipable
    
    def give_weapon_not_equipable(self, weapon):
        self.weapons[weapon.id] = weapon

        return weapon.id

    def give_weapon_equipable(self, weapon):
        self.weapons[weapon.id] = weapon

        if (
            self.sets_weapon.get_equiped_weapon(hand='main') is None and
            self.sets_weapon.get_equiped_weapon(hand='both') is None
        ):
            self.sets_weapon.equip_weapon(weapon)
        elif (
            self.sets_weapon.get_equiped_weapon(hand='off') is None and
            self.sets_weapon.get_equiped_weapon(hand='both') is None and
            'off' in weapon.get_handed()
        ):
            self.sets_weapon.equip_weapon(weapon, hand='off')

        return weapon.id


class SetsWeapon(object):
    def __init__(self, rack_weapon=None):
        self.rack_weapon = rack_weapon
        
        self.active_weapon_set = 1
        self.active_weapon_set_both = False

        self.weapon_sets = {
                1: {
                    'main': None,
                    'off': None,
                    'both': None,
                },
                2: {
                    'main': None,
                    'off': None,
                    'both': None,
                },
            }
    
    def equip_weapon_by_id(self, weapon_id, hand='main', weapon_set=0):
        if weapon_id in self.rack_weapon.weapons.keys():
            self.equip_weapon(
                    weapon=self.rack_weapon.weapons[weapon_id],
                    hand=hand,
                    weapon_set=weapon_set,
                )

    def equip_weapon(self, weapon, hand='main', weapon_set=0):
        if weapon_set == 0:
            weapon_set = self.active_weapon_set
        if weapon_set < 0 or weapon_set > 2:
            weapon_set = 1
        if hand not in ('main', 'off', 'both'):
            hand = 'main'

        if hand == 'main' or hand == 'off':
            self.weapon_sets[weapon_set]['both'] = None
        elif hand == 'both':
            self.weapon_sets[weapon_set]['main'] = None
            self.weapon_sets[weapon_set]['off'] = None

        self.weapon_sets[weapon_set][hand] = weapon
        self._set_is_wielding_both_handed()

    def get_equiped_weapon(self, hand='main'):
        return self.weapon_sets[self.active_weapon_set][hand]

    def switch_weapon_set(self, weapon_set=0):
        new_active = 1

        if weapon_set == 1:
            new_active = 2
        elif weapon_set == 2:
            new_active = 1
        else:
            if self.active_weapon_set == 1:
                new_active = 2
            else:
                new_active = 1

        self.active_weapon_set = new_active

        self.set_is_wielding_both_handed()

        return new_active

    def _set_is_wielding_both_handed(self):
        if self.get_equiped_weapon(hand='both') is None:
            self.active_weapon_set_both = False
        else:
            self.active_weapon_set_both = True
