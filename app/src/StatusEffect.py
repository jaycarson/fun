#!/usr/bin/python


class StatusEffects(object):
    def __init__(self):
        return

    def get_status_effect(self, name, actor, target, power):
        if name == 'hot':
            status_effect = Hot(actor, target, power)
        elif name == 'dot':
            status_effect = Dot(actor, target, power)
        return status_effect


class StatusEffect(object):
    def __init__(self, actor, target, power):
        self.name = 'None'
        self.power = power
        self.actor, target = actor, target


class Dot(StatusEffect):
    def __init__(self, actor, target, power):
        StatusEffect.__init__(self, actor, target, power)
        self.name = 'Damage Over Time'


class Hot(StatusEffect):
    def __init__(self, actor, target, power):
        StatusEffect.__init__(self, actor, target, power)
        self.name = 'Heal Over Time'


class Burn(Dot):
    def __init__(self, actor, target, power):
        Dot.__init__(self, actor, target, power):
        self.name = 'Burn'
        self.damage_tick = 0

    def trigger(self):
        self.target.take_damage(self.damage_tick)
