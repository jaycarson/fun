#!/usr/bin/python

from random import choice
from Components import Levelable
from Components import Skillable
from Components import RackArmor
from Components import RackWeapon

from Character import Character, CharacterVPC, CharacterNPC, CharacterPC

from Library import BookStat


class Faction(object):
    def __init__(self,
                 experience=0,
                 name='None',
                 faction_id=0,
                 clock=None,  # Clock Object
                 smithy_weapon=None,
                 smithy_armor=None,
                 brains=None
                 ):
        self.faction_id = faction_id
        self.races = ['human']
        self.book_stat = BookStat()

        self.skillable = Skillable()
        self.levelable = Levelable(
                    exp=experience,
                    skillable=self.skillable,
                )
        self.rack_armor = RackArmor()
        self.rack_weapon = RackWeapon()

        self.name = name
        self.clock = clock
        self.characters = []
        self.brains = brains
        self.smithy_weapon = smithy_weapon
        self.smithy_armor = smithy_armor

    def get_level(self):
        return self.levelable.get_level()

    def get_world_time(self):
        return self.clock.get_world_time()

    def give_experience(self, experience):
        self.levelable.give_exp(experience)

    def get_experience(self):
        return self.levelable.exp

    def activate(self, character):
        global_cooldown = 1000
        self.brains[character.get_brain()].act(character)
        return character.gcd

    def place_char(self, character, locations):
        looking = True

        while looking:
            location = choice(locations)
            if location.character is None:
                location.character = character
                character.dungeon_hex = location
                looking = False

    def create_vpc(self, name='any', race='any'):
        if race == 'any' or race not in self.races:
            race = choice(self.races)

        new_stats = self.book_stat.generate_for_character()

        new_character = CharacterVPC(
                experience=0,
                race=race,
                name=name,
                char_id=name,
                stats=new_stats,  # Dictionary
            )

        new_character.faction = self

        self.equip_standard_character(new_character)

        self.characters.append(new_character)

        return new_character

    def equip_standard_character(self, character):
        self.equip_standard_weapon(character)
        self.equip_standard_armor(character)

    def equip_standard_weapon(self, character):
        default_weapon = self.smithy_weapon.create(
                    weapon='club',
                    quality='common',
                    color='whilte',
                )

        character.rack_weapon.give_weapon(default_weapon)

    def equip_standard_armor(self, character):
        for piece in self.smithy_armor._armor_pieces:
            default_piece = self.smithy_armor.create(
                    armor_type='cloth',
                    armor_piece=piece,
                    quality='common',
                    skills=None,
                )

            character.rack_armor.give_armor(default_piece)



class FactionPC(Faction):
    def __init__(self, experience=0, race='human', name='None'):
        Faction.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
        )


class FactionNPC(Faction):
    def __init__(self, experience=0, race='human', name='None'):
        Faction.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
        )


class FactionVPC(Faction):
    def __init__(self, experience=0, race='human', name='None'):
        Faction.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
        )
