#!/usr/bin/python

from Abilities import Abilities
from Weapon import Weapon
from Armor import Armor
from Dice import Dice

from random import seed
from random import choice
from random import randint


class Smithy(object):
    def __init__(self, library):
        self.library = library

        self.loaded = {
                'armor': False,
                'weapon': False,
                'regiment armor': False,
                'regiment weapon': False,
            }

        self.smiths = {
                'armor': None,
                'weapon': None,
                'regiment armor': None,
                'regiment weapon': None,
            }

    def get_smith(self, smith):
        smith = smith.lower()

        assert smith in self.smiths

        if self.loaded[smith] is False:
            self.smiths[smith] = self.wake_smith(smith)
            self.loaded[smith] = True

        return self.smiths[smith]

    def wake_smith(self, smith):
        if smith == 'armor':
            return SmithArmor(self.library)
        elif smith == 'weapon':
            return SmithWeapon(self.library)
        elif smith == 'regiment armor':
            return SmithRegimentArmor(self.library)
        elif smith == 'regiment weapon':
            return SmithRegimentWeapon(self.library)


class Smith(object):
    def __init__(self, library):
        self.library = library
        self.book_stat = self.library.get_book('stat')
        self.book_quality = self.library.get_book('quality')
        self.book_color = self.library.get_book('color')
        self.book_dice = self.library.get_book('dice')

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
    def __init__(self, library):
        Smith.__init__(self, library)

        self.book_armor = self.library.get_book('armor')
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
            stats=self.book_stat.generate_for_gear(
                    quality=quality,
                    piece=armor_piece,
                    armor_type=armor_type,
                ),
            armor_id=self.generate_id(),
            dice=self.get_dice(color),
            )

        return armor


class SmithWeapon(Smith):
    def __init__(self, library):
        Smith.__init__(self, library)
        self.book_weapon = self.library.get_book('weapon')
        self.book_skill = self.library.get_book('skill')
        self.weapons = self.book_weapon.get_weapon_list()
        self.abilities = Abilities(self.library)

    def create(self,
               weapon='any',
               quality='any',
               color='any',
               ):
        weapon_type = weapon
        if weapon_type == 'any' or weapon_type not in self.weapons:
            weapon_type = choice(self.weapons)
        if quality == 'any' or quality not in self.qualities:
            quality = choice(self.qualities)
        if color == 'any' or color not in self.colors:
            color = choice(self.colors)

        damage_type = self.book_weapon.get_weapon_damage_type(weapon_type)
        damage_types = []
        damage_types.append(damage_type)

        new_weapon = Weapon()
        new_weapon.weapon_type = weapon_type
        new_weapon.quality = quality
        new_weapon.color = color
        new_weapon.skills = self.book_weapon.get_weapon_skills(weapon_type)
        new_weapon.handed = self.book_weapon.get_weapon_handed(weapon_type)
        new_weapon.damage_types = damage_types
        new_weapon.stats = self.book_stat.generate_for_gear(quality)
        
        new_weapon.id = self.generate_id()

        new_weapon.add_dice(self.get_dice(color))

        self.add_ability_set_to_weapon(
                weapon=new_weapon,
                set_name='simple',
                skills=['simple'],
            )

        return new_weapon

    def add_ability_set_to_weapon(self, weapon, set_name, skills):
        ability_set = self.generate_ability_set(
                        damage_types=weapon.damage_types,
                        skills=skills,
                    )
        strength_set = self.generate_strength_set()
        cooldown_set = self.generate_cooldown_set(strength_set)
        
        weapon.add_ability_set(set_name, ability_set, strength_set)

    def generate_ability_set(self, damage_types, skills=['simple']):
        skill_list = []
        skill_list_primary = []
        ability_set = []

        for skill in skills:
            for damage_type in damage_types:
                skill_list_primary += self.book_skill.get_skill_abilities_primary(
                    skill=skill,
                    damage_type=damage_type,
                    )

        for skill in skills:
            for damage_type in damage_types:
                skill_list += self.book_skill.get_skill_abilities(
                    skill=skill,
                    damage_type=damage_type,
                    )

        ability = self.get_ability_primary(choice(skill_list_primary))
        ability_set.append(ability)

        for counter in range(0, 4):
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

    def get_ability(self, ability_name):
        return self.abilities.get_ability(ability_name)
    
    def get_ability_primary(self, ability_name):
        return self.abilities.get_ability_primary(ability_name)
