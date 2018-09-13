#!/usr/bin/python

from Library import BookStat


class Abilities(object):
    def __init__(self):
        self.abilities = {
                'advance': Advance(),
                'blow': Blow(),
                'cut': Cut(),
                'double_chop': DoubleChop(),
                'final_thrust': FinalThrust(),
                'flurry': Flurry(),
                'gash': Gash(),
                'jab': Jab(),
                'rip': Rip(),
                'skull_crack': SkullCrack(),
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

        self.primary_abilities = {
                'bash': Bash(),
                'chop': Chop(),
                'slash': Slash(),
                'stab': Stab(), #
            }

    def get_ability(self, name):
        return self.abilities[name]


class Ability(object):
    def __init__(self):
        self.name = 'None'
        self.one_second = 1000
        self.cd = self.one_second  # Cool Down
        self.gcd = self.one_second  # Global Cool Down
        self.combat_type = 'melee'
        self.combat_role = 'damage'
        self.range = 1
        self.damage_type = 'physical'
        self.base_scaling = 1
        self.min_gcd = self.one_second / 2
        self.max_cd = self.one_second * 60
        self.can_attack_on_move = True
        self.primary_attribute = 'force'
        self.secondary_attribute = 'athletic'
        self.base_stat = BookStat().base
        self.max_stat = self.base_stat * 2
        self.cycle = self.noncyclable

    def activate(self, actor, slot):
        target_enemy = actor.target_enemy
        target_ally = actor.target_ally
        power = actor.get_power(slot)
        cycle = actor.get_cycle(slot)
        current_time = actor.get_time()
        distance = actor.distance_to_enemy

        cooldown_added = 0

        if target_enemy is not None:
            target_enemy.take_damage(
                    self.calc_damage(actor, power, slot, cycle),
                    self.damage_type,
                )

            actor.take_gcd(cooldown=self.calc_gcd(actor, power, slot, cycle))
            cooldown_added = self.calc_cooldown(actor, power, slot, cycle)

        return cooldown_added + current_time

    def activate_hyp(self, actor, slot):
        target_enemy = actor.target_enemy
        target_ally = actor.target_ally
        power = actor.get_power(slot)
        cycle = actor.get_cycle(slot)
        current_time = actor.get_time()
        distance = actor.distance_to_enemy

        if distance > self.get_range(actor, power, slot, cycle):
            return 0
        else:
            damage = self.calc_damage(actor, power, slot, cycle)
            time = self.calc_gcd(actor, power, slot, cycle) / float(self.one_second)
            dps = damage / time
            return dps

    def get_range(self, actor, power, slot, cycle):
        return self.calc_range(actor, power, slot, cycle)

    def get_base_damage(self, actor):
        return actor.get_attack_dice() * 10 * self.base_scaling

    def get_base_defense(self, actor):
        return actor.get_defense_dice() * 10 * self.base_scaling

    def get_base_morale(self, actor):
        return actor.get_morale_dice() * 10 * self.base_scaling

    def get_cooldown(self, actor, power, slot, cycle, cooldown_adj):
        cooldown = self.calc_cooldown(actor, power, slot, cycle)

        if isinstance(cooldown_adj, float):
            cooldown = int(self.cd * cooldown_adj)
        else:
            cooldown = self.cd + cooldown_adj

        return cooldown

    def calc_damage(self, actor, power, slot, cycle):
        base_damage = self.get_base_damage(actor)
        slot_damage = base_damage * slot * 0.5
        power_damage = base_damage * power * 0.5
        primary = actor.get_full_stat(self.primary_attribute)
        stat_damage = base_damage * primary / self.max_stat
        total_damage = int(
                    base_damage +
                    slot_damage +
                    power_damage +
                    stat_damage
                )
        return total_damage

    def calc_range(self, actor, power, slot, cycle):
        return self.range

    def calc_cooldown(self, actor, power, slot, cycle):
        if slot == 0:
            return 0
        else:
            slot_penalty = self.cd * slot * 5
            power_bonus = self.cd * power * 5
            secondary = actor.get_stat(self.secondary_attribute) / 2
            stat_bonus = self.cd * secondary / self.max_stat
            cooldown = int(
                    self.cd +
                    slot_penalty -
                    power_bonus -
                    stat_bonus
                )
            return min(cooldown, self.max_cd)

    def calc_gcd(self, actor, power, slot, cycle):
        secondary = actor.get_stat(self.secondary_attribute) / 2
        power_bonus = 1 - power
        slot_bonus = 0
        stat_bonus = 1 - (secondary/self.max_stat/4)
        cooldown = int(
                self.gcd *
                stat_bonus *
                power_bonus -
                slot_bonus
            )
        return max(int(self.gcd * power_bonus - slot_bonus), self.min_gcd)

    def cyclable(self, cycle):
        if cycle == 3:
            cycle = 1
        else:
            cycle += 1

        return cycle

    def noncyclable(self, cycle):
        return cycle


class Stab(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Stab'
        self.cycle = self.cyclable


class Bash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Bash'
        self.cycle = self.cyclable

    def calc_damage(self, actor, power, slot):
        return self.base_damage * 1.1

    def calc_cooldown(self, actor, power, slot):
        return self.cd


class Chop(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Chop'
        self.cycle = self.cyclable


class Slash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Slash'
        self.cycle = self.cyclable


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
