#!/usr/bin/python


class Weapon(object):
    def __init__(self,
                 weapon_type,
                 quality,
                 color,
                 skills,
                 handed,
                 damage,
                 stats,
                 ability_set,
                 weapon_id,
                 ):
        self._weapon_type = weapon_type
        self._quality = quality
        self._color = color
        self._skills = skills  # List
        self._handed = handed  # List
        self._damage = damage
        self._stats = stats

        self._ability_sets = {}
        self._ability_sets['simple'] = ability_set
        self._active_set = 'simple'
        self._owner = None
        self._id = weapon_id

    def get_id(self):
        return self._id

    def get_weapon_type(self):
        return self._weapon_type

    def get_slot_ability(self, slot):
        return self._ability_sets[self._active_set][slot]

    def get_quality(self):
        return self._quality

    def get_color(self):
        return self._color

    def get_handed(self):
        return self._handed

    def set_owner(self, owner):
        self._owner = owner

        for ability_set_name in self.get_ability_set_names():
            for ability in self.get_ability_set(ability_set_name):
                ability.set_owner(owner)

    def on_cooldown(self, slot):
        ability = self.get_active_ability_set()[slot]

        if ability.on_cooldown():
            return True
        else:
            return False

    def activate(self, slot):
        return self._ability_sets[self._active_set][slot].activate()

    def get_stat(self, stat_name):
        assert stat_name in self._stats
        return self._stats[stat_name]

    def get_ability_set_names(self):
        abilities = []

        for key in self._ability_sets.keys():
            abilities.append(key)

        return abilities

    def add_ability_set(self, ability_set, ability_set_name):
        self._ability_sets[ability_set_name] = ability_set

    def get_active_ability_set(self):
        return self._ability_sets[self._active_set]

    def get_ability_set(self, ability_set_name):
        return self._ability_sets[ability_set_name]
