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
                 cd_timer_set,
                 cd_adj_set,
                 strength_set,
                 weapon_id,
                 ):
        self.weapon_type = weapon_type
        self.quality = quality
        self.color = color
        self.skills = skills  # List
        self.handed = handed  # List
        self.damage = damage
        self.stats = stats

        self.ability_sets = {}
        self.cd_timers = {}
        self.strengths = {}
        self.cd_adjs = {}
        self.ability_sets['simple'] = ability_set
        self.active_set = 'simple'
        self.id = weapon_id
        self.cd_timers['simple'] = cd_timer_set
        self.cd_adjs['simple'] = cd_adj_set
        self.strengths['simple'] = strength_set

    def get_slot_ability(self, slot):
        return self.ability_sets[self.active_set][slot]

    def get_combat_type(self):
        return self.ability_sets[self.active_set][0].combat_type

    def get_combat_role(self):
        return self.ability_sets[self.active_set][0].combat_role

    def on_cooldown(self, slot, current_time):
        return self.cd_timers[self.active_set][slot] > current_time

    def activate(self, actor, slot, current_time, distance):
        ability = self.ability_sets[self.active_set][slot]
        strength = self.strengths[self.active_set][slot]
        cd_adj = self.cd_adjs[self.active_set][slot]
        self.cd_timers[self.active_set][slot] = ability.activate(
                actor=actor,
                power=strength,
                slot=slot,
                current_time=current_time,
                distance=distance,
                cd_adj=cd_adj,
            )

    def activate_hyp(self, actor, slot, current_time, distance):
        ability = self.ability_sets[self.active_set][slot]
        strength = self.strengths[self.active_set][slot]
        cd_adj = self.cd_adjs[self.active_set][slot]
        return ability.activate_hyp(
                actor=actor,
                power=strength,
                slot=slot,
                current_time=current_time,
                distance=distance,
                cd_adj=cd_adj,
            )

    def get_stat(self, stat_name):
        assert stat_name in self.stats
        return self.stats[stat_name]

    def get_ability_set_names(self):
        abilities = []

        for key in self.ability_sets.keys():
            abilities.append(key)

        return abilities

    def add_ability_set(self, ability_set, ability_set_name):
        self.ability_sets[ability_set_name] = ability_set

    def get_active_ability_set(self):
        return self.ability_sets[self.active_set]

    def get_ability_set(self, ability_set_name):
        return self.ability_sets[ability_set_name]

    def get_active_ability_slot(self, slot):
        active_set = self.get_active_ability_set()
        return active_set[slot]
