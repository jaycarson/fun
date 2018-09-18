#!/usr/bin/python

import yaml
from random import randint
from random import choice
from sets import Set


class BookConst(object):
    def __init__(self):
        self.full_stats = 1000

        self.stats = Set([
            'might',
            'athletic',
            'reflex',
            'initiative',
            'knowledge',
            'reason',
            'faith',
            'perception',
            'endurance',
            'fortitude',
            'presence',
            'willpower',
        ])

        self.stat_count = len(self.stats)
        
        self.colors = Set([
            'red',
            'purple',
            'blue',
            'green',
            'yellow',
            'orange',
            'white',
        ])

        self.armor_pieces = Set([
            'belt',
            'chest',
            'gloves',
            'helm',
            'pants',
            'ring',
            'shoes',
            'shoulders',
        ])

        self.armor_count = len(self.armor_pieces)

        self.armor_types = Set([
            'cloth',
            'leather',
            'studded',
            'chain',
            'plate',
        ])


class BookColor(object):
    def __init__(self):
        self._list = [
            'red',
            'purple',
            'blue',
            'green',
            'yellow',
            'orange',
            'white',
        ]

    def get_list(self):
        return self._list

    def get_color(self, color):
        if color not in self._list:
            return choice(self._list)
        else:
            return color


class BookQuality(object):
    def __init__(self):
        self.book_const = BookConst()

        total_set_stats = (
                self.book_const.full_stats / self.book_const.armor_count
            )

        common = total_set_stats / 2.0
        uncommon = common + total_set_stats / 4.0
        rare = uncommon + total_set_stats / 8.0
        epic = rare + total_set_stats / 16.0
        legendary = epic + total_set_stats / 32.0

        self._qual = {
            'common':  int(common),
            'uncommon': int(uncommon),
            'rare': int(rare),
            'epic': int(epic),
            'legendary': int(legendary),
        }

        self._list_of_qualities = []

        for key in self._qual.keys():
            self._list_of_qualities.append(key)

    def get_qualities(self):
        return self._qual

    def get_quality(self, quality):
        quality = quality.lower()
        assert quality in self._qual.keys()
        return self._qual[quality]

    def get_list_of_qualities(self):
        return self._list_of_qualities

    def get_list(self):
        return self._list_of_qualities


class BookStat(object):
    def __init__(self, base=80):
        self.stats = {
            'might': base,
            'athletic': base,
            'reflex': base,
            'initiative': base,
            'knowledge': base,
            'reason': base,
            'faith': base,
            'perception': base,
            'endurance': base,
            'fortitude': base,
            'presence': base,
            'willpower': base,
        }

        self.zero_stats = {
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
        }

        self.book_quality = BookQuality()
        self.base = base

        self.list_of_stats = []

        for key in self.stats.keys():
            self.list_of_stats.append(key)

    def set_stat(self, stat, value):
        assert stat in self.stats.keys()
        self.stats[stat] = value

    def get_stats(self):
        return self.stats

    def get_base_stat(self):
        return self.base

    def get_stat(self, stat):
        assert stat in self._stats.keys()
        return self.stats[stat]

    def get_list(self):
        return self.list_of_stats

    def generate_for_gear(self, quality):
        assert quality in self.book_quality.get_list_of_qualities()

        total_stat_weight = self.book_quality.get_quality(quality)
        remainder = total_stat_weight

        gear_stats = self.zero_stats.copy()

        list_of_stats = list(self.list_of_stats)

        number_of_stats = randint(1, 5)

        remaining_number = number_of_stats

        for stat in range(0, number_of_stats):
            stat = choice(list_of_stats)
            list_of_stats.remove(stat)

            if(remaining_number <= 1):
                gear_stats[stat] = remainder
                remaining_stats = 0
            elif(remainder > 1):
                min_rand = int(remainder/2)
                max_rand = int(remainder/4) * 3

                if max_rand <= min_rand:
                    max_rand = min_rand + 1

                this_stat = randint(min_rand, max_rand)

                remainder -= this_stat

                gear_stats[stat] = this_stat

            remaining_number -= 1

        return gear_stats

    def generate_for_character(self):
        character_stats = {}

        for stat in self.get_list():
            character_stats[stat] = self.base

        return character_stats


class BookWeapon(object):
    def __init__(self):
        weapon_path = "../rsc/Books/Weapons.yml"
        self._weapons = yaml.load(open(weapon_path))

        self._damage_types = [
            'bludgeon',
            'chop',
            'pierce',
            'slash',
        ]

        self._weapon_list = []

        for weapon in self._weapons.keys():
            self._weapon_list.append(weapon)

    def get_damage_types(self):
        return self._damage_types

    def get_weapons(self):
        return self._weapons

    def get_weapon(self, weapon):
        return self._weapons[weapon]

    def get_weapon_list(self):
        return self._weapon_list

    def get_weapon_skills(self, weapon):
        return self._weapons[weapon]['skills']

    def get_weapon_damage_type(self, weapon):
        return self._weapons[weapon]['damage']

    def get_weapon_handed(self, weapon):
        return self._weapons[weapon]['handed']


class BookDice(object):
    def __init__(self):
        book_path = "../rsc/Books/Dice.yml"
        self.dice_book = yaml.load(open(book_path))

    def get_attack(self, color):
        return self.dice_book[color]['attack']

    def get_defense(self, color):
        return self.dice_book[color]['defense']

    def get_morale(self, color):
        return self.dice_book[color]['morale']


class BookArmor(object):
    def __init__(self):
        self._pieces = [
            'belt',
            'chest',
            'gloves',
            'helm',
            'pants',
            'ring',
            'shoes',
            'shoulders',
        ]

        self._types = [
            'cloth',
            'leather',
            'studded',
            'chain',
            'plate',
        ]

    def get_pieces(self):
        return self._pieces

    def get_types(self):
        return self._types


class BookSkill(object):
    def __init__(self):
        skill_path = "../rsc/Books/Skills.yml"
        self._skills = yaml.load(open(skill_path))

        self._skill_list = [
            'martial',
            'simple',
            'light-weapon',
            'finesse',
            'range',
            'reach',
            'thrown',
            'heavy',
            'engineer',
            'hunt',
            'fire',
            'earth',
            'water',
            'air',
            'light',
            'dark',
            'life',
            'death',
            'spirit',
            'blood',
        ]

        self._weapon_types = BookWeapon().get_weapon_list()
        self._damage_types = BookWeapon().get_damage_types()

    def get_skill_abilities(self, skill='Any', damage_type='Any'):
        if skill == 'Any' or skill not in self._skill_list:
            skill = choice(self._skill_list)
        if damage_type == 'Any' or damage_type not in self._damage_types:
            damage_type = choice(self._damage_types)

        damage_type = damage_type + "_abilities"

        return self._skills[skill][damage_type]

    def get_skill_abilities_primary(self, skill='Any', damage_type='Any'):
        if skill == 'Any' or skill not in self._skill_list:
            skill = choice(self._skill_list)
        if damage_type == 'Any' or damage_type not in self._damage_types:
            damage_type = choice(self._damage_types)

        damage_type = damage_type + "_primary_abilities"

        return self._skills[skill][damage_type]

    def get_list(self):
        return self._list_of_skills


class BookAtlas(object):
    def __init__(self):
        self._terrain_types = [
            'Hill',
            'Island',
            'Mountains',
            'Plain',
            'Volcano',
            'Volcanic Island',
            'Unknown',
        ]

        self._flora_types = [
            'Desert',
            'Tundra',
            'Coniferous',
            'Deciduous',
            'Rainforest',
            'Wasteland',
            'Shrubland',
            'Bog',
            'Marsh',
            'Swamp',
            'Plains',
            'Mangrove',
            'Unknown',
        ]

        self._tile_sides = [
            'n',
            'ne',
            'nw',
            's',
            'se',
            'sw',
        ]

    def get_terrain_types(self):
        return self._terrain_types

    def get_flora_types(self):
        return self._flora_types

    def get_tile_sides(self):
        return self._tile_sides


class BookGeography(object):
    def __init__(self):
        path = "../rsc/Books/Geography.yml"
        self._book = yaml.load(open(path))
        self._terrain_types = self._book['types']
        self._flora_types = self._book['flora']
        self._dists = self._book['dists']

        self._tile_sides = [
            'n',
            'ne',
            'nw',
            's',
            'se',
            'sw',
        ]

    def get_terrain_types(self):
        return self._terrain_types

    def get_flora_types(self):
        return self._flora_types

    def get_tile_sides(self):
        return self._tile_sides

