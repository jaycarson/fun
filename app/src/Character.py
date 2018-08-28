#!/usr/bin/python

from Library import BookArmor


class Character(object):
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

        self.race = race
        self.name = name
        self.clock = clock
        self.local_id = 0

        self.stats = stats

        self.weapons = {}
        self.armors = {}

        self.target_enemy = None
        self.target_ally = None

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

        self.skills = []
        self.skill_points_current = 0
        self.skill_points_total = 0

        self.armors_by_piece = {}
        self.armors_equiped_by_piece = {}

        for piece in BookArmor().get_pieces():
            self.armors_by_piece[piece] = {}
            self.armors_equiped_by_piece[piece] = None

    def get_level(self):
        level = self.experience / 1000

        if level > 40:
            level = 40

        return level

    def get_stat(self, stat):
        return self.stats.get(stat)

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
        weapon.set_owner(self)

        if (
            self.get_equiped_weapon(hand='main') is None and
            self.get_equiped_weapon(hand='both') is None
        ):
            self.equip_weapon(weapon)
        elif (
            self.get_equiped_weapon(hand='off') is None and
            self.get_equiped_weapon(hand='both') is None and
            'off' in weapon.get_handed()
        ):
            self.equip_weapon(weapon, hand='off')

        return weapon_id

    def give_armor(self, armor):
        armor_id = armor.get_id()
        self.armors[armor.get_id()] = armor

        piece = armor.get_piece()
        self.armors_by_piece[piece][armor_id] = armor

        if self.get_equiped_armor(piece) is None:
            self.equip_armor(armor)

        return armor_id

    def give_experience(self, experience):
        starting_level = self.get_level()

        self.experience += experience

        current_level = self.get_level()

        if current_level > starting_level:
            levels_gained = current_level - starting_level
            for x in range(0, levels_gained):
                self._gain_level()

    def equip_weapon_by_id(self, weapon_id, hand='main', weapon_set=0):
        if weapon_id in self.weapons.keys():
            self.equip_weapon(
                    weapon=self.weapons[weapon_id],
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

    def attack(self, slot=1):
        ws = self.active_weapon_set

        if self.active_weapon_set_both:
            self.weapon_sets[ws]['both'].activate(slot)
        elif slot <= 3:
            self.weapon_sets[ws]['main'].activate(slot)
        elif slot <= 5:
            self.weapon_sets[ws]['off'].activate(slot)

    def equip_armor(self, armor):
        piece = armor.get_piece()
        self.armors_equiped_by_piece[piece] = armor

    def get_equiped_armor(self, piece='chest'):
        return self.armors_equiped_by_piece[piece]

    def activate(self, dungeon_master):
        global_cooldown = 1000
        self.global_cooldown = self.get_local_time() + global_cooldown
        return self.global_cooldown
