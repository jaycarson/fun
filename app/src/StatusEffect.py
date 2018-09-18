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
        self.damage_type = None
        self.ticks = 1
        self.damage_tick = 0


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


class Bleed(Dot):
    def __init__(self, power):
        Dot.__init__(self, power)
        self.name = 'Bleed'
        self.daamge_type = 'physical'
        self.ticks = min(10 + int(self.power/30), 20)
        self.damage_tick = int(self.power/self.ticks)

    def trigger(self, host):
        host.take_damage(self.damage_tick, self.damage_type)
        self.ticks -= 1


class Burn(Dot):
    def __init__(self, power):
        Dot.__init__(self, power)
        self.name = 'Burn'
        self.daamge_type = 'fire'
        self.ticks = max(20 - int(self.power/100), 5)
        self.damage_tick = int(self.power/self.ticks)

    def trigger(self, host):
        host.take_damage(self.damage_tick, self.damage_type)
        self.ticks -= 1


class Buff(StatusEffect):
    def __init__(self, power):
        StatusEffect.__init__(self, power)
        self.name = 'Buff'
        self.ticks = 1
    
    def trigger(self, host):
        self.ticks -= 1


class BuffStat(Buff):
    def __init__(self, power, name='might'):
        Buff.__init__(self, power)
        self.name = name.capitalize()
        self.effect = name
        self.ticks = 10 + power / 10
    
    def trigger(self, host):
        self.ticks -= 1
        host.status_count[self.effect] += 1


class Interfere(StatusEffect):
    def __init__(self, power):
        StatusEffect.__init__(self, power)
        self.name = 'Interfere'
        self.ticks = 1

    def trigger(self, host):
        self.ticks -= 1
        delay = self.power / 1000

        if host.casting:
            host.cast_time += delay


class Snare(StatusEffect):
    def __init__(self, power):
        StatusEffect.__init__(self, power)
        self.name = 'Snare'
        self.effect = 'snare'
        self.ticks = 10 + power / 100

    def trigger(self, host):
        self.ticks -= 1
        host.status_count[self.effect] += 1


class Vulnerability(StatusEffect):
    def __init__(self, power):
        StatusEffect.__init__(self, power)
        self.name = 'Vulnerability'
        self.effect = 'vulnerability'
        self.ticks = 10 + power / 100

    def trigger(self, host):
        self.ticks -= 1
        host.status_count[self.effect] += 1
