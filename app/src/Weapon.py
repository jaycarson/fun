#!/usr/bin/python


class Weapon(object):
    def __init__(self):
        self.weapon_type = ''
        self.quality = ''
        self.color = ''
        self.skills = []  # List
        self.handed = []  # List
        self.damage = ''
        self.damage_types = []
        self.stats = {}

        self.ability_sets = {}
        self.cd_timers = {}
        self.strengths = {}
        self.id = 0

        self.cycles = {}
        
        self.dice = None
        self.dice_both_handed = None

    def add_ability_set(self, name, ability_set, strength_set):
        self.strengths[name] = strength_set
        self.ability_sets[name] = ability_set
        self.cycles[name] = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1}
        self.cd_timers[name] = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

        self.active_set = name

    def add_dice(self, dice, dice_both_handed=None):
        self.dice = dice
        self.dice_both_handed = dice_both_handed
        
        self.dice.roll()

        if dice_both_handed is not None:
            self.dice_both_handed.roll()

    def get_slot_ability(self, slot):
        return self.ability_sets[self.active_set][slot]

    def get_combat_type(self):
        return self.ability_sets[self.active_set][0].combat_type

    def get_combat_role(self):
        return self.ability_sets[self.active_set][0].combat_role

    def on_cooldown(self, slot, current_time):
        return self.cd_timers[self.active_set][slot] > current_time

    def activate(self, actor, slot):
        ability = self.ability_sets[self.active_set][slot]
        
        new_cooldown = ability.activate(actor=actor, slot=slot)
        
        self.cd_timers[self.active_set][slot] = new_cooldown
        
        current_cycle = self.cycles[self.active_set][slot]
        next_cycle = ability.cycle(current_cycle)
        self.cycles[self.active_set][slot] = next_cycle

    def activate_hyp(self, actor, slot):
        current_cd = self.cd_timers[self.active_set][slot]

        if current_cd > actor.get_time():
            return -1

        ability = self.ability_sets[self.active_set][slot]

        if actor.moved and not ability.can_attack_on_move:
            return -1

        return ability.activate_hyp(actor=actor, slot=slot)

    def get_stat(self, stat_name):
        assert stat_name in self.stats
        return self.stats[stat_name]

    def get_ability_set_names(self):
        abilities = []

        for key in self.ability_sets.keys():
            abilities.append(key)

        return abilities

    def get_active_ability_set(self):
        return self.ability_sets[self.active_set]

    def get_ability_set(self, ability_set_name):
        return self.ability_sets[ability_set_name]

    def get_active_ability_slot(self, slot):
        active_set = self.get_active_ability_set()
        return active_set[slot]
    
    def roll_dice(self):
        return self.dice.roll()

    def get_dice_face(self):
        return self.dice.get_value()

    def set_dice_face(self, face):
        self.dice.value = face
    
    def roll_dice_both_handed(self):
        return self.dice_both_handed.roll()

    def get_dice_face_both_handed(self):
        return self.dice_both_handed.get_value(self)

    def set_dice_face_both_handed(self, face):
        self.dice_both_handed.value = face
