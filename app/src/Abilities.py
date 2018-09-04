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
        self.cd = 1  # Cool Down
        self.gcd = 1  # Global Cool Down

    def calc_cooldown(self, cooldown_adj):
        if isinstance(cooldown_adj, float):
            cooldown = int(self.cooldown * cooldown_adj)
        else:
            cooldown = self.cd + cooldown_adj

        return cooldown

    def activate(self, actor, power, cooldown, current_time):
        target_enemy = actor.target_enemy
        target_ally = actor.target_ally
        
        return self.calc_cooldown(cooldown) + current_time


class Bash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.name = 'Bash'


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
