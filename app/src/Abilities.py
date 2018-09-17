#!/usr/bin/python

from Library import BookStat
from StatusEffect import Damage


class Abilities(object):
    def __init__(self):
        self.abilities = {
                'advance': Advance(),
                'blow': Blow(),
                'cut': Cut(),
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
                'wild_blow': WildBlow(),
                'whirl': Whirl(),
            }

        self.primary_abilities = {
                'bash': Bash(),
                'chop': Chop(),
                'slash': Slash(),
                'stab': Stab(),
            }

    def get_ability(self, name):
        return self.abilities[name]

    def get_ability_primary(self, name):
        return self.primary_abilities[name]


class Ability(object):
    def __init__(self):
        self.name_1 = 'None'
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
        self.damage_multiplier = 1.0

    def activate(self, actor, slot):
        target_enemy = actor.target_enemy
        target_ally = actor.target_ally
        current_time = actor.get_time()

        cooldown_added = 0

        if target_enemy is not None:
            target_enemy.receive_status_effects(self.get_effects(actor, slot))

            actor.take_gcd(cooldown=self.calc_gcd(actor, slot))
            cooldown_added = self.calc_cooldown(actor, slot)

        return cooldown_added + current_time

    def activate_hyp(self, actor, slot):
        distance = actor.distance_to_enemy

        if distance > self.get_range(actor, slot):
            return 0
        else:
            damage = self.calc_damage(actor, slot)
            time = self.calc_gcd(actor, slot) / float(self.one_second)
            dps = damage / time
            return dps

    def get_name(self, actor, slot):
        return self.name_1

    def get_range(self, actor, slot):
        return self.calc_range(actor, slot)

    def get_base_damage(self, actor):
        return actor.get_attack_dice() * 10 * self.base_scaling

    def get_base_defense(self, actor):
        return actor.get_defense_dice() * 10 * self.base_scaling

    def get_base_morale(self, actor):
        return actor.get_morale_dice() * 10 * self.base_scaling

    def get_cooldown(self, actor, slot):
        cooldown = self.calc_cooldown(actor, slot)

        if isinstance(cooldown_adj, float):
            cooldown = int(self.cd * cooldown_adj)
        else:
            cooldown = self.cd + cooldown_adj

        return cooldown

    def calc_damage(self, actor, slot):
        power = actor.get_power(slot)
        base_damage = self.get_base_damage(actor)
        slot_damage = base_damage * slot * 0.5
        power_damage = base_damage * power * 0.5
        primary = actor.get_full_stat(self.primary_attribute)
        stat_damage = base_damage * primary / self.max_stat
        total_damage = (
                    base_damage +
                    slot_damage +
                    power_damage +
                    stat_damage
                )
        return int(total_damage * self.damage_multiplier)

    def calc_range(self, actor, slot):
        return self.range

    def calc_cooldown(self, actor, slot):
        power = actor.get_power(slot)
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

    def calc_gcd(self, actor, slot):
        power = actor.get_power(slot)
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

    def cycle(self, cycle):
        return cycle

    def get_effects(self, actor, slot):
        return [
            Damage(
                power=self.calc_damage(actor, slot),
                damage_type='physical',
                ),
            ]


class AbilityCyclable(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'None'
        self.name_2 = 'None'
        self.name_3 = 'None'
        self.cycle_1_modifier = 0.75
        self.cycle_2_modifier = 1.25
        self.cycle_3_modifier = 1.75

    def get_name(self, actor, slot):
        cycle = actor.get_cycle(slot)

        if cycle == 1:
            name = self.name_1
        elif cycle == 2:
            name = self.name_2
        else:
            name = self.name_3

        return name

    def cycle(self, cycle):
        if cycle == 3:
            cycle = 1
        else:
            cycle += 1

        return cycle

    def calc_damage(self, actor, slot):
        power = actor.get_power(slot)
        base_damage = self.get_base_damage(actor)
        slot_damage = base_damage * slot * 0.5
        power_damage = base_damage * power * 0.5
        primary = actor.get_full_stat(self.primary_attribute)
        stat_damage = base_damage * primary / self.max_stat
        total_damage = (
                    base_damage +
                    slot_damage +
                    power_damage +
                    stat_damage
                )
        
        cycle = actor.get_cycle(slot)
        
        if cycle == 1:
            total_damage *= self.cycle_1_modifier
        elif cycle == 2:
            total_damage *= self.cycle_2_modifier
        elif cycle == 3:
            total_damage *= self.cycle_3_modifier
        
        return int(total_damage * self.damage_multiplier)

    def get_effects(self, actor, slot):
        cycle = actor.get_cycle(slot)
        effects = []
        
        if cycle == 1:
            effects = self.get_cycle_1_effects(actor, slot)
        elif cycle == 2:
            effects = self.get_cycle_2_effects(actor, slot)
        elif cycle == 3:
            effects = self.get_cycle_3_effects(actor, slot)

        return effects

    def get_cycle_1_effects(self, actor, slot):
        return [
            Damage(
                power=self.calc_damage(actor, slot),
                damage_type='physical',
                ),
            ]

    def get_cycle_2_effects(self, actor, slot):
        return [
            Damage(
                power=self.calc_damage(actor, slot),
                damage_type='physical',
                ),
            ]

    def get_cycle_3_effects(self, actor, slot):
        return [
            Damage(
                power=self.calc_damage(actor, slot),
                damage_type='physical',
                ),
            ]


class Stab(AbilityCyclable):
    def __init__(self):
        AbilityCyclable.__init__(self)
        self.name_1 = 'Stab'
        self.name_2 = 'Double Stab'
        self.name_3 = 'Tripple Stab'


class Bash(AbilityCyclable):
    def __init__(self):
        AbilityCyclable.__init__(self)
        self.name_1 = 'Bash'
        self.name_2 = 'Double Bash'
        self.name_3 = 'Triple Bash'


class Chop(AbilityCyclable):
    def __init__(self):
        AbilityCyclable.__init__(self)
        self.name_1 = 'Chop'
        self.name_2 = 'Double Chop'
        self.name_3 = 'Triple Chop'


class Slash(AbilityCyclable):
    def __init__(self):
        AbilityCyclable.__init__(self)
        self.name_1 = 'Slash'
        self.name_2 = 'Double Slash'
        self.name_3 = 'Triple Slash'


class FinalThrust(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Final Thrust'


class Gash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Gash'


class Hamstring(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Hamstring'


class Hit(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Hit'


class Impale(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Impale'


class Rip(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Rip'


class Ripost(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Ripost'


class Rush(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Rush'


class SavageLeap(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Savage Leap'


class SeverArtery(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Sever Artery'


class Swing(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Swing'


class Slice(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Slice'


class Gash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Gash'


class WildSlash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Wild Slash'


class Strike(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Strike'


class WildStrike(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Wild Strike'


class WildSwing(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Wild Swing'


class Smack(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Smack'


class Blow(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Blow'


class SkullCrack(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Skull Crack'


class WildBlow(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Wild Blow'


class Thrust(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Thrust'


class Jab(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Jab'


class WildThrust(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Wild Thrust'


class Advance(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Advance'


class Cut(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Cut'


class Flurry(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Flurry'


class Whirl(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Whirl'


class WildBash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name_1 = 'Wild Bash'
