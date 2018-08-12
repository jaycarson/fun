#!/usr/bin/python

from Library import BookColor
from Library import BookQuality
from Library import BookStat
from Library import BookWeapon
from Library import BookArmor
from Library import BookSkill

from Abilities import FinalThrust
from Abilities import Gash
from Abilities import Hamstring
from Abilities import Hit
from Abilities import Impale
from Abilities import Rip
from Abilities import Ripost
from Abilities import Rush
from Abilities import SavageLeap
from Abilities import SeverArtery
from Abilities import Swing
from Abilities import Slash
from Abilities import Slice
from Abilities import Gash
from Abilities import WildSlash
from Abilities import Strike
from Abilities import WildStrike
from Abilities import Smack
from Abilities import Blow
from Abilities import SkullCrack
from Abilities import WildBlow
from Abilities import Bash
from Abilities import WildBash
from Abilities import Thrust
from Abilities import Jab
from Abilities import WildThrust
from Abilities import Advance
from Abilities import Chop
from Abilities import DoubleChop
from Abilities import TripleChop
from Abilities import Cut
from Abilities import Flurry
from Abilities import Whirl

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

    def _generate_id(self):
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
               piece='any',
               quality='any',
               color='any',
               armor_piece='any',
               skills=None,
               ):
        if armor_type == 'any' or armor_type not in self._armor_types:
            armor_type = choice(self._armor_types)
        if piece == 'any' or piece not in self._pieces:
            piece = choice(self._armor_pieces)
        if quality == 'any' or quality not in self._qualities:
            quality = choice(self._qualities)
        if color == 'any' or color not in self._colors:
            color = choice(self._colors)
        if armor_piece == 'any' or armor_piece not in self._armor_pieces:
            armor_piece = choice(self._armor_pieces)

        armor = Armor(
            armor_type=armor_type,
            piece=piece,
            quality=quality,
            color=color,
            skills=skills,
            stats=self._book_stat.generate_for_gear(quality),
            armor_id=self._generate_id(),
            )

        return armor


class SmithWeapon(Smith):
    def __init__(self):
        Smith.__init__(self)
        self._book_weapon = BookWeapon()
        self._book_skill = BookSkill()
        self._weapons = self._book_weapon.get_weapon_list()

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

        return Weapon(
            weapon_type=weapon,
            quality=quality,
            color=color,
            skills=self._book_weapon.get_weapon_skills(weapon),
            handed=self._book_weapon.get_weapon_handed(weapon),
            damage=damage_types,
            stats=self._book_stat.generate_for_gear(quality),
            ability_set=self._generate_ability_set(damage_types),
            weapon_id=self._generate_id(),
            )

    def _generate_ability_set(self, damage_types, skills=['simple']):
        skill_list = []
        ability_set = []

        for skill in skills:
            for damage_type in damage_types:
                skill_list += self._book_skill.get_skill_abilities(
                    skill=skill,
                    damage_type=damage_type,
                    )

        power_set = self._generate_power_set()

        for power in power_set:
            ability = self._get_ability(choice(skill_list))
            ability.set_power(power)
            ability_set.append(ability)

        return ability_set

    def _generate_power_set(self):
        p1 = randint(1, 5)
        p2 = randint(2, 10)
        p3 = randint(3, 10)
        p4 = randint(4, 10)
        p5 = randint(5, 10)
        total = p1 + p2 + p3 + p4 + p5

        power_set = [
            int(p1 / total * 10),
            int(p2 / total * 10),
            int(p3 / total * 10),
            int(p4 / total * 10),
            int(p5 / total * 10),
            ]

        return power_set

    def _get_ability(self, ability_name):
        ability = 'None'

        if ability_name == 'final_thrust':
            ability = FinalThrust()
        elif ability_name == 'gash':
            ability = Gash()
        elif ability_name == 'hamstring':
            ability = Hamstring()
        elif ability_name == 'impale':
            ability = Impale()
        elif ability_name == 'rip':
            ability = Rip()
        elif ability_name == 'ripost':
            ability = Ripost()
        elif ability_name == 'rush':
            ability = Rush()
        elif ability_name == 'savage_leap':
            ability = SavageLeap()
        elif ability_name == 'sever_artery':
            ability = SeverArtery()
        elif ability_name == 'swing':
            ability = Swing()
        elif ability_name == 'slash':
            ability = Slash()
        elif ability_name == 'slice':
            ability = Slice()
        elif ability_name == 'gash':
            ability = Gash()
        elif ability_name == 'wild_slash':
            ability = WildSlash()
        elif ability_name == 'strike':
            ability = Strike()
        elif ability_name == 'wild_strike':
            ability = WildStrike()
        elif ability_name == 'smack':
            ability = Smack()
        elif ability_name == 'blow':
            ability = Blow()
        elif ability_name == 'skull_crack':
            ability = SkullCrack()
        elif ability_name == 'wild_blow':
            ability = WildBlow()
        elif ability_name == 'bash':
            ability = Bash()
        elif ability_name == 'wild_bash':
            ability = WildBash()
        elif ability_name == 'thrust':
            ability = Thrust()
        elif ability_name == 'jab':
            ability = Jab()
        elif ability_name == 'wild_thrust':
            ability = WildThrust()
        elif ability_name == 'advance':
            ability = Advance()
        elif ability_name == 'chop':
            ability = Chop()
        elif ability_name == 'double_chop':
            ability = DoubleChop()
        elif ability_name == 'triple_chop':
            ability = TripleChop()
        elif ability_name == 'cut':
            ability = Cut()
        elif ability_name == 'flurry':
            ability = Flurry()
        elif ability_name == 'whirl':
            ability = Whirl()
        else:
            ability = Hit()

        return ability
