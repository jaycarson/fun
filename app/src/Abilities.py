#!/usr/bin/python


class Abilities(object):
    def __init__(self):
        self.abilities = {
                'advance': Advance(),
                'bash': Bash(),
                'blow': Blow(),
                'chop': Chop(),
                'cut': Cut(),
                'double_chop': DoubleChop(),
                'final_thrust': FinalThrust(),
                'flurry': Flurry(),
                'gash': Gash(),
                'jab': Jab(),
                'rip': Rip(),
                'skull_crack': SkullCrack(),
                'slash': Slash(),
                'slice': Slice(),
                'smack': Smack(),
                'strike': Strike(),
                'thrust': Thrust(),
                'swing': Swing(),
                'wild_bash': WildBash(),
                'wild_slash': WildSlash(),
                'wild_strike': WildStrike(),
                'wild_swing': WildSwing(),
                'wild_thrust': WildThrust(),
                'triple_chop': TripleChop(),
                'wild_blow': WildBlow(),
                'whirl': Whirl(),
            }

    def get_ability(self, name):
        return self.abilities[name]


class Ability(object):
    def __init__(self):
        self.name = 'None'
        self.cd = 1000  # Cool Down
        self.gcd = 1000  # Global Cool Down
        self.combat_type = 'melee'
        self.combat_role = 'damage'
        self.range = 1
        self.base_damage = 100
        self.damage_type = 'physical'
        self.min_gcd = 500
        self.max_cd = 60000
        self.can_attack_on_move = True

    def activate(
            self,
            actor,
            power,
            slot,
            current_time,
            distance,
            cd_adj,
            ):
        target_enemy = actor.target_enemy
        target_ally = actor.target_ally
        cooldown_added = 0

        if target_enemy is not None:
            target_enemy.take_damage(
                    self.calc_damage(power, slot),
                    self.damage_type,
                )

            actor.take_gcd(cooldown=self.calc_gcd(power, slot))
            cooldown_added = self.calc_cooldown(power, slot)

        return cooldown_added + current_time

    def activate_hyp(
            self,
            actor,
            power,
            slot,
            current_time,
            distance,
            cd_adj,
            ):
        if distance > self.get_range(actor, power, slot):
            return 0
        else:
            return self.calc_damage(power, slot)

    def get_range(self, actor, power, slot):
        return self.calc_range(power, slot)

    def get_cooldown(self, actor, power, slot, cooldown_adj):
        cooldown = self.calc_cooldown(power)

        if isinstance(cooldown_adj, float):
            cooldown = int(self.cd * cooldown_adj)
        else:
            cooldown = self.cd + cooldown_adj

        return cooldown

    def calc_damage(self, power, slot):
        slot_damage = self.base_damage * slot * 0.5
        power_damage = self.base_damage * power * 0.5
        return int(self.base_damage + slot_damage + power_damage)

    def calc_range(self, power, slot):
        return self.range

    def calc_cooldown(self, power, slot):
        if slot == 0:
            return 0
        else:
            slot_penalty = self.cd * slot * 5
            power_bonus = self.cd * power * 5
            return min(int(self.cd + slot_penalty - power_bonus), self.max_cd)

    def calc_gcd(self, power, slot):
        power_bonus = 1 - power
        slot_bonus = 0
        return max(int(self.gcd * power_bonus - slot_bonus), self.min_gcd)


class Bash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Bash'

    def calc_damage(self, power, slot):
        return self.base_damage * 1.1

    def calc_cooldown(self, power, slot):
        return self.cd


class FinalThrust(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Final Thrust'


class Gash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Gash'


class Hamstring(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Hamstring'


class Hit(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Hit'


class Impale(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Impale'


class Rip(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Rip'


class Ripost(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Ripost'


class Rush(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Rush'


class SavageLeap(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Savage Leap'


class SeverArtery(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Sever Artery'


class Swing(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Swing'


class Slash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Slash'


class Slice(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Slice'


class Gash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Gash'


class WildSlash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Wild Slash'


class Strike(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Strike'


class WildStrike(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Wild Strike'


class WildSwing(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Wild Swing'


class Smack(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Smack'


class Blow(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Blow'


class SkullCrack(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Skull Crack'


class WildBlow(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Wild Blow'


class Thrust(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Thrust'


class Jab(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Jab'


class WildThrust(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Wild Thrust'


class Advance(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Advance'


class Chop(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Chop'


class DoubleChop(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'DoubleChop'


class TripleChop(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Triple Chop'


class Cut(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Cut'


class Flurry(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Flurry'


class Whirl(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Whirl'


class WildBash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Wild Bash'
