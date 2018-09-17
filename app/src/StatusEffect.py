#!/usr/bin/python


class StatusEffects(object):
    def __init__(self):
        return

    def get_status_effect(self, name, power, damage_type='physical'):
        if name == 'damage':
            status_effect = Damage(power, damage_type)
        if name == 'hot':
            status_effect = Hot(power)
        elif name == 'dot':
            status_effect = Dot(power)
        return status_effect

    def trigger(self, host):
        return


class StatusEffect(object):
    def __init__(self, power):
        self.name = 'None'
        self.power = power


class Damage(StatusEffect):
    def __init__(self, power, damage_type):
        StatusEffect.__init__(self, power)
        self.name = 'Damage'
        self.damage_type = damage_type
        self.ticks = 1
        self.damage_tick = self.power

    def trigger(self, host):
        host.take_damage(self.damage_tick, self.damage_type)
        self.ticks -= 1


class Dot(StatusEffect):
    def __init__(self, power):
        StatusEffect.__init__(self, power)
        self.dot_benefit = 1.25
        self.power = int(self.power * self.dot_benefit)
        self.name = 'Damage Over Time'
        self.ticks = 10
        self.damage_tick = int(self.power / self.ticks)

    def trigger(self, host):
        host.take_damage(self.damage_tick, self.damage_type)
        self.ticks -= 1


class Hot(StatusEffect):
    def __init__(self, power):
        StatusEffect.__init__(self, power)
        self.name = 'Heal Over Time'

    def trigger(self, host):
        self.ticks -= 1


class Burn(Dot):
    def __init__(self, power):
        Dot.__init__(self, power)
        self.name = 'Burn'
        self.daamge_type = 'fire'
        self.ticks = 10 + int(self.power/100)
        self.damage_tick = int(self.power/self.ticks)

    def trigger(self, host):
        host.take_damage(self.damage_tick, self.damage_type)
        self.ticks -= 1
