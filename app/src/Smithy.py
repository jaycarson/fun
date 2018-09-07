#!/usr/bin/python

from Library import BookColor
from Library import BookQuality
from Library import BookStat
from Library import BookWeapon
from Library import BookArmor
from Library import BookSkill

from Abilities import Abilities
from Weapon import Weapon
from Armor import Armor

from random import seed
from random import choice
from random import randint


class Smithy(object):
    def __init__(self):
        self._book_weapons = BookWeapon()
        self._book_quality = BookQuality()

        self._weapon_types = self._book_wepaon.get_types()
        self._qualities = self._book_quality.get_qualities()

        self._book = BookSkill()

        self._smith_sword = SmithWeaponSword(self._book)

    def set_seed(self, new_seed):
        seed(new_seed)

    def create(self, category='Any', name='Any', quality='Any'):
        if category == 'Any':
            weapon_type = choice(self._weapon_types)
        if quality == 'Any':
            quality = choice(self._qualities)

        if weapon_type == 'Axe':
            return self._sword_smith.create(weapon_name)
        elif weapon_type == 'Mace':
            return self._sword_smith.create(weapon_name)
        elif weapon_type == 'Sword':
            return self._sword_smith.create(weapon_name)
        else:
            return self._sword_smith.create(weapon_name)


class Smith(object):
    def __init__(self):
        self._book_stat = BookStat()
        self._book_quality = BookQuality()
        self._book_color = BookColor()

        self._colors = self._book_color.get_list()

        self._qualities = self._book_quality.get_list_of_qualities()
        self._stat_weights = self._book_quality.get_qualities()

        self._ids = []
        self._max_rand_id = 10000000

    def set_seed(self, seed):
        random.seed(seed)

    def create(self):
        return 1

    def generate_color(self, color='Any'):
        if color == 'Any':
            color = choice(self._colors)
        return color

    def generate_id(self):
        new_id = randint(1, self._max_rand_id)

        while new_id in self._ids:
            new_id = randint(1, self._max_rand_id)

        self._ids.append(new_id)

        return new_id


class SmithArmor(Smith):
    def __init__(self):
        Smith.__init__(self)

        self._book_armor = BookArmor()
        self._armor_pieces = self._book_armor.get_pieces()
        self._armor_types = self._book_armor.get_types()

    def set_seed(self, seed):
        random.seed(seed)

    def create(self,
               armor_type='any',
               quality='any',
               color='any',
               armor_piece='any',
               skills=None,
               ):
        if armor_type == 'any' or armor_type not in self._armor_types:
            armor_type = choice(self._armor_types)
        if quality == 'any' or quality not in self._qualities:
            quality = choice(self._qualities)
        if color == 'any' or color not in self._colors:
            color = choice(self._colors)
        if armor_piece == 'any' or armor_piece not in self._armor_pieces:
            armor_piece = choice(self._armor_pieces)

        armor = Armor(
            armor_type=armor_type,
            piece=armor_piece,
            quality=quality,
            color=color,
            skills=skills,
            stats=self._book_stat.generate_for_gear(quality),
            armor_id=self.generate_id(),
            )

        return armor


class SmithWeapon(Smith):
    def __init__(self):
        Smith.__init__(self)
        self._book_weapon = BookWeapon()
        self._book_skill = BookSkill()
        self._weapons = self._book_weapon.get_weapon_list()
        self._abilities = Abilities()

    def create(self,
               weapon='any',
               quality='any',
               color='any',
               ):
        if weapon == 'any' or weapon not in self._weapons:
            weapon = choice(self._weapons)
        if quality == 'any' or quality not in self._qualities:
            quality = choice(self._qualities)
        if color == 'any' or color not in self._colors:
            color = choice(self._colors)

        damage_type = self._book_weapon.get_weapon_damage_type(weapon)
        damage_types = []
        damage_types.append(damage_type)

        ability_set = self.generate_ability_set(damage_types)
        strength_set = self.generate_strength_set()
        cooldown_set = self.generate_cooldown_set(strength_set)
        cooldown_adj_set = self.generate_cooldown_adj_set(strength_set)

        return Weapon(
            weapon_type=weapon,
            quality=quality,
            color=color,
            skills=self._book_weapon.get_weapon_skills(weapon),
            handed=self._book_weapon.get_weapon_handed(weapon),
            damage=damage_types,
            stats=self._book_stat.generate_for_gear(quality),
            ability_set=ability_set,
            cd_timer_set=cooldown_set,
            cd_adj_set=cooldown_adj_set,
            strength_set=strength_set,
            weapon_id=self.generate_id(),
            )

    def generate_ability_set(self, damage_types, skills=['simple']):
        skill_list = []
        ability_set = []

        for skill in skills:
            for damage_type in damage_types:
                skill_list += self._book_skill.get_skill_abilities(
                    skill=skill,
                    damage_type=damage_type,
                    )

        for counter in range(0, 5):
            ability = self.get_ability(choice(skill_list))
            ability_set.append(ability)

        return ability_set

    def generate_strength_set(self):
        p1 = randint(1, 5)
        p2 = randint(2, 10)
        p3 = randint(3, 10)
        p4 = randint(4, 10)
        p5 = randint(5, 10)
        total = p1 + p2 + p3 + p4 + p5

        power_set = {
                0: int(p1 / total * 10),
                1: int(p2 / total * 10),
                2: int(p3 / total * 10),
                3: int(p4 / total * 10),
                4: int(p5 / total * 10),
            }

        return power_set

    def generate_cooldown_set(self, strength_set):
        cooldown_set = {}
        
        for slot in strength_set.keys():
            cooldown_set[slot] = 0
        
        return cooldown_set

    def generate_cooldown_adj_set(self, strength_set):
        return {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

    def get_ability(self, ability_name):
        return self._abilities.get_ability(ability_name)
