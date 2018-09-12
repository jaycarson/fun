#!/usr/bin/python

from Library import BookColor
from Library import BookQuality
from Library import BookStat
from Library import BookWeapon
from Library import BookArmor
from Library import BookSkill
from Library import BookDice

from Abilities import Abilities
from Weapon import Weapon
from Armor import Armor
from Dice import Dice

from random import seed
from random import choice
from random import randint


class Smithy(object):
    def __init__(self):
        self.book_weapons = BookWeapon()
        self.book_quality = BookQuality()

        self.weapon_types = self.book_wepaon.get_types()
        self.qualities = self.book_quality.get_qualities()

        self.book = BookSkill()

        self.smith_sword = SmithWeaponSword(self.book)

    def set_seed(self, new_seed):
        seed(new_seed)

    def create(self, category='Any', name='Any', quality='Any'):
        if category == 'Any':
            weapon_type = choice(self.weapon_types)
        if quality == 'Any':
            quality = choice(self.qualities)

        if weapon_type == 'Axe':
            return self.sword_smith.create(weapon_name)
        elif weapon_type == 'Mace':
            return self.sword_smith.create(weapon_name)
        elif weapon_type == 'Sword':
            return self.sword_smith.create(weapon_name)
        else:
            return self.sword_smith.create(weapon_name)


class Smith(object):
    def __init__(self):
        self.book_stat = BookStat()
        self.book_quality = BookQuality()
        self.book_color = BookColor()
        self.book_dice = BookDice()

        self.colors = self.book_color.get_list()

        self.qualities = self.book_quality.get_list_of_qualities()
        self.stat_weights = self.book_quality.get_qualities()

        self.ids = []
        self.max_rand_id = 10000000

    def set_seed(self, seed):
        random.seed(seed)

    def create(self):
        return 1

    def generate_color(self, color='Any'):
        if color == 'Any':
            color = choice(self.colors)
        return color

    def generate_id(self):
        new_id = randint(1, self.max_rand_id)

        while new_id in self.ids:
            new_id = randint(1, self.max_rand_id)

        self.ids.append(new_id)

        return new_id

    def get_dice(self, color):
        return Dice(
                attack=self.book_dice.get_attack(color),
                defense=self.book_dice.get_defense(color),
                morale=self.book_dice.get_morale(color),
            )


class SmithArmor(Smith):
    def __init__(self):
        Smith.__init__(self)

        self.book_armor = BookArmor()
        self.armor_pieces = self.book_armor.get_pieces()
        self.armor_types = self.book_armor.get_types()

    def set_seed(self, seed):
        random.seed(seed)

    def create(self,
               armor_type='any',
               quality='any',
               color='any',
               armor_piece='any',
               skills=None,
               ):
        if armor_type == 'any' or armor_type not in self.armor_types:
            armor_type = choice(self.armor_types)
        if quality == 'any' or quality not in self.qualities:
            quality = choice(self.qualities)
        if color == 'any' or color not in self.colors:
            color = choice(self.colors)
        if armor_piece == 'any' or armor_piece not in self.armor_pieces:
            armor_piece = choice(self.armor_pieces)

        armor = Armor(
            armor_type=armor_type,
            piece=armor_piece,
            quality=quality,
            color=color,
            skills=skills,
            stats=self.book_stat.generate_for_gear(quality),
            armor_id=self.generate_id(),
            dice=self.get_dice(color),
            )

        return armor


class SmithWeapon(Smith):
    def __init__(self):
        Smith.__init__(self)
        self.book_weapon = BookWeapon()
        self.book_skill = BookSkill()
        self.weapons = self.book_weapon.get_weapon_list()
        self.abilities = Abilities()

    def create(self,
               weapon='any',
               quality='any',
               color='any',
               ):
        if weapon == 'any' or weapon not in self.weapons:
            weapon = choice(self.weapons)
        if quality == 'any' or quality not in self.qualities:
            quality = choice(self.qualities)
        if color == 'any' or color not in self.colors:
            color = choice(self.colors)

        damage_type = self.book_weapon.get_weapon_damage_type(weapon)
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
            skills=self.book_weapon.get_weapon_skills(weapon),
            handed=self.book_weapon.get_weapon_handed(weapon),
            damage=damage_types,
            stats=self.book_stat.generate_for_gear(quality),
            ability_set=ability_set,
            cd_timer_set=cooldown_set,
            cd_adj_set=cooldown_adj_set,
            strength_set=strength_set,
            weapon_id=self.generate_id(),
            dice=self.get_dice(color),
            )

    def generate_ability_set(self, damage_types, skills=['simple']):
        skill_list = []
        ability_set = []

        for skill in skills:
            for damage_type in damage_types:
                skill_list += self.book_skill.get_skill_abilities(
                    skill=skill,
                    damage_type=damage_type,
                    )

        for counter in range(0, 5):
            ability = self.get_ability(choice(skill_list))
            ability_set.append(ability)

        return ability_set

    def generate_strength_set(self):
        p1 = randint(1, 10)
        p2 = randint(1, 10)
        p3 = randint(1, 10)
        p4 = randint(1, 10)
        p5 = randint(1, 10)
        total = float(p1 + p2 + p3 + p4 + p5)

        power_set = {
                0: p1 / total,
                1: p2 / total,
                2: p3 / total,
                3: p4 / total,
                4: p5 / total,
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
        return self.abilities.get_ability(ability_name)
