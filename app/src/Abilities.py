#!/usr/bin/python

from StatusEffect import Damage, Bleed, BuffStat, Interfere, Snare, Vulnerability


class Abilities(object):
    def __init__(self, library):
        self.library = library
        self.abilities = {
                'advance': Advance(self.library),
                'blow': Blow(self.library),
                'cut': Cut(self.library),
                'final_thrust': FinalThrust(self.library),
                'flurry': Flurry(self.library),
                'gash': Gash(self.library),
                'jab': Jab(self.library),
                'rip': Rip(self.library),
                'skull_crack': SkullCrack(self.library),
                'slice': Slice(self.library),
                'smack': Smack(self.library),
                'strike': Strike(self.library),
                'thrust': Thrust(self.library),
                'swing': Swing(self.library),
                'wild_bash': WildBash(self.library),
                'wild_slash': WildSlash(self.library),
                'wild_strike': WildStrike(self.library),
                'wild_swing': WildSwing(self.library),
                'wild_thrust': WildThrust(self.library),
                'wild_blow': WildBlow(self.library),
                'whirl': Whirl(self.library),
            }

        self.primary_abilities = {
                'bash': Bash(self.library),
                'chop': Chop(self.library),
                'slash': Slash(self.library),
                'stab': Stab(self.library),
            }

    def get_ability(self, name):
        return self.abilities[name]

    def get_ability_primary(self, name):
        return self.primary_abilities[name]

    def get_regiment_ability(self, name):
        return self.regiment_abilities[name]


class Ability(object):
    def __init__(self, library):
        self.library = library
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
        self.primary_attribute = 'might'
        self.secondary_attribute = 'athletic'
        self.base_stat = self.library.get_book('const').full_stats / 2
        self.max_stat = self.base_stat * 2
        self.damage_multiplier = 1.0

    def activate(self, actor, slot):
        target_enemy = actor.target_enemy
        target_ally = actor.target_ally
        current_time = actor.get_time()

        cooldown_added = 0

        if target_enemy is not None:
            self.give_effects(actor, slot)

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

    def activate_regiment(self, actor, slot):
        current_time = actor.get_time()
        cooldown = 0
        
        if slot == 1:
            cooldown = self.activate_regiment_attack(actor)
        elif slot == 2:
            cooldown = self.activate_regiment_move_forward(actor)
        elif slot == 3:
            cooldown = self.activate_regiment_turn_left(actor)
        elif slot == 4:
            cooldown = self.activate_regiment_turn_right(actor)
        elif slot == 5:
            cooldown = self.activate_regiment_charge(actor)

        return cooldown + current_time

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
        total_damage *= self.damage_multiplier
        return int(total_damage)

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

    def give_effects(self, actor, slot):
        debuffs = [
            Damage(
                power=self.calc_damage(actor, slot),
                damage_type='physical',
                ),
            ]

        actor.target_enemy.receive_status_effects(debuffs)

    def activate_regiment_attack(self, actor):
        enemies = actor.dm.get_adjacent_enemies(actor)
        cooldown = 0

        if len(enemies) > 0:
            for enemy in enemies:
                self.regiment_give_effects(actor, enemy)
        elif actor.target_enemy is not None:
            ability_range = int(self.calc_range(actor, slot=1)/self.scaling)
            if ability_range > 1:
                self.regiment_give_effects(actor, 1)

            actor.take_gcd(cooldown=self.calc_gcd(actor, 1))
            cooldown = self.calc_cooldown(actor, 1)

        return cooldown

    def activate_regiment_move_forward(self, actor):
        new_hex = actor.dm.get_neighboring_hex(actor, actor.facing)

        if actor.dm.is_neighboring_hex_empty(actor, actor.facing):
            actor.move(actor.dm.get_neighboring_hex(actor, actor.facing))
            speed = actor.regiment_speed / self.standard_speed
            cooldown = speed * self.one_second
            return cooldown

        return 0

    def activate_regiment_turn_left(self, actor):
        new_facing = actor.facing - 1
        if new_facing == -1:
            new_facting = 5
        actor.facing =  new_facing

        speed = actor.regiment_speed / self.standard_speed
        cooldown = speed * self.one_second / 4
        return cooldown
                
    def activate_regiment_turn_right(self, actor):
        new_facing = actor.facing + 1
        if new_facing == 6:
            new_facting = 0
        actor.facing =  new_facing

        speed = actor.regiment_speed / self.standard_speed
        cooldown = speed * self.one_second / 4
        return cooldown
                    
    def activate_regiment_charge(self, actor):
        adjacent_enemies = actor.dm.get_adjacent_enemies(actor)

        if len(adjacent_enemies) > 0:
            return 0

        chargable_enemies = actor.dm_get_enemies_in_line(
                requestor=actor,
                direction=actor.facing,
                distance=actor.regiment_charge_range,
            )

        if len(chargable_enemies) == 0:
            return 0

        for movement in range(0, actor.regiment_charge_range + 1):
            self.activate_regiment_move_forward(actor)

        self.regiment_give_effects_charge(actor, 1)

        speed = actor.regiment_speed / self.standard_speed
        cooldown = speed * self.one_second
        return cooldown


class AbilityCyclable(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
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
       
        total_damage *= self.damage_multiplier
        return int(total_damage)

    def give_effects(self, actor, slot):
        cycle = actor.get_cycle(slot)
        effects = []
        
        if cycle == 1:
            self.give_cycle_1_effects(actor, slot)
        elif cycle == 2:
            self.give_cycle_2_effects(actor, slot)
        elif cycle == 3:
            self.give_cycle_3_effects(actor, slot)

        return effects

    def give_cycle_1_effects(self, actor, slot):
        debuffs = [
            Damage(
                power=self.calc_damage(actor, slot),
                damage_type='physical',
                ),
            ]

        actor.target_enemy.receive_status_effects(debuffs)

    def give_cycle_2_effects(self, actor, slot):
        debuffs = [
            Damage(
                power=self.calc_damage(actor, slot),
                damage_type='physical',
                ),
            ]

        actor.target_enemy.receive_status_effects(debuffs)

    def give_cycle_3_effects(self, actor, slot):
        debuffs = [
            Damage(
                power=self.calc_damage(actor, slot),
                damage_type='physical',
                ),
            ]

        actor.target_enemy.receive_status_effects(debuffs)


class Stab(AbilityCyclable):
    def __init__(self, library):
        AbilityCyclable.__init__(self, library)
        self.name_1 = 'Stab'
        self.name_2 = 'Double Stab'
        self.name_3 = 'Tripple Stab'

    def give_cycle_2_effects(self, actor, slot):
        power = self.calc_damage(actor, slot)
        
        buffs = [
                BuffStat(power=power, name='initiative'),
            ]

        debuffs = [
                Damage(power=power, damage_type='physical'),
            ]

        actor.receive_status_effects(buffs)
        actor.target_enemy.receive_status_effects(debuffs)

    def give_cycle_3_effects(self, actor, slot):
        power = self.calc_damage(actor, slot)
        
        debuffs = [
                Damage(power=power/2, damage_type='physical'),
                Bleed(power=power/2),
            ]
        
        actor.target_enemy.receive_status_effects(debuffs)


class Bash(AbilityCyclable):
    def __init__(self, library):
        AbilityCyclable.__init__(self, library)
        self.name_1 = 'Bash'
        self.name_2 = 'Double Bash'
        self.name_3 = 'Triple Bash'

    def give_cycle_2_effects(self, actor, slot):
        power = self.calc_damage(actor, slot)
        
        buffs = [
                BuffStat(power=power, name='endurance'),
            ]

        debuffs = [
                Damage(power=power * 3 / 4, damage_type='physical'),
                Interfere(power=power/2),
            ]

        actor.receive_status_effects(buffs)
        actor.target_enemy.receive_status_effects(debuffs)

    def give_cycle_3_effects(self, actor, slot):
        power = self.calc_damage(actor, slot)
        
        debuffs = [
                Damage(power=power * 3 /4, damage_type='physical'),
                Interfere(power=power),
            ]
        
        actor.target_enemy.receive_status_effects(debuffs)


class Chop(AbilityCyclable):
    def __init__(self, library):
        AbilityCyclable.__init__(self, library)
        self.name_1 = 'Chop'
        self.name_2 = 'Double Chop'
        self.name_3 = 'Triple Chop'

    def give_cycle_2_effects(self, actor, slot):
        power = self.calc_damage(actor, slot)
        
        buffs = [
                BuffStat(power=power, name='might'),
            ]

        debuffs = [
                Damage(power=power, damage_type='physical'),
            ]

        actor.receive_status_effects(buffs)
        actor.target_enemy.receive_status_effects(debuffs)

    def give_cycle_3_effects(self, actor, slot):
        power = self.calc_damage(actor, slot)
        
        debuffs = [
                Damage(power=power * 3/4, damage_type='physical'),
                Snare(power=power/2),
            ]
        
        actor.target_enemy.receive_status_effects(debuffs)


class Slash(AbilityCyclable):
    def __init__(self, library):
        AbilityCyclable.__init__(self, library)
        self.name_1 = 'Slash'
        self.name_2 = 'Double Slash'
        self.name_3 = 'Triple Slash'

    def get_cycle_2_effects(self, actor, slot):
        power = self.calc_damage(actor, slot)
        
        buffs = [
                BuffStat(power=power, name='reflex'),
            ]

        debuffs = [
                Damage(power=power * 3/4, damage_type='physical'),
                Vulnerability(power=power/2),
            ]

        actor.receive_status_effects(buffs)
        actor.target_enemy.receive_status_effects(debuffs)


class FinalThrust(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Final Thrust'


class Gash(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Gash'


class Hamstring(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Hamstring'


class Hit(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Hit'


class Impale(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Impale'


class Rip(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Rip'


class Ripost(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Ripost'


class Rush(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Rush'


class SavageLeap(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Savage Leap'


class SeverArtery(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Sever Artery'


class Swing(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Swing'


class Slice(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Slice'


class Gash(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Gash'


class WildSlash(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Wild Slash'


class Strike(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Strike'


class WildStrike(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Wild Strike'


class WildSwing(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Wild Swing'


class Smack(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Smack'


class Blow(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Blow'


class SkullCrack(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Skull Crack'


class WildBlow(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Wild Blow'


class Thrust(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Thrust'


class Jab(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Jab'


class WildThrust(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Wild Thrust'


class Advance(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Advance'


class Cut(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Cut'


class Flurry(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Flurry'


class Whirl(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Whirl'


class WildBash(Ability):
    def __init__(self, library):
        Ability.__init__(self, library)
        self.name_1 = 'Wild Bash'
