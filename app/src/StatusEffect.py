#!/usr/bin/python


class StatusEffects(object):
    def __init__(self):
        return

    def get_status_effect(self, name, power):
        if name == 'damage':
            status_effect = Damage(power)
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
        self.primary_attribute = 'force'
        self.daamge_type = 'physical'
        self.power = power


class Damage(StatusEffect):
    def __init__(self, power):
        StatusEffect.__init__(self, power)
        self.name = 'Damage'
        self.ticks = 0
        self.damage_tick = power

    def trigger(self, host):
        host.take_damage(self.damage_tick)


class Dot(StatusEffect):
    def __init__(self, power):
        StatusEffect.__init__(self, power)
        self.name = 'Damage Over Time'
        self.ticks = 10
        self.damage_tick = int(power / self.ticks)

    def trigger(self, host):
        host.take_damage(self.damage_tick)


class Hot(StatusEffect):
    def __init__(self, power):
        StatusEffect.__init__(self, power)
        self.name = 'Heal Over Time'


class Burn(Dot):
    def __init__(self, power):
        Dot.__init__(self, power)
        self.name = 'Burn'
        self.daamge_type = 'fire'
        self.ticks = 10 + int(power/100)
        self.damage_tick = int(power/self.ticks)

    def trigger(self, host):
        host.take_damage(self.damage_tick)
