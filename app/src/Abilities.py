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
        self._owner = None
        self._name = 'None'
        self._ability_cooldown = 1
        self._cooldown = 0
        self._power = 1

    def set_owner(self, owner):
        self._owner = owner

    def set_power(self, power):
        self._power = power

    def on_cooldown(self):
        if self._owner.get_locale_time() < self._cooldown:
            return True
        else:
            return False

    def activate(self):
        if self.on_cooldown():
            return

        self._cooldown = self._owner.get_locale_time() + self._ability_cooldown
        self._activate()

    def _activate(self):
        target_enemy = self._owner.target_enemy
        target_ally = self._owner.target_ally
        return

    def get_current_time(self):
        return self._owner.get_current_time()

    def get_name(self):
        return self._name


class Bash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Bash'


class FinalThrust(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Final Thrust'


class Gash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Gash'


class Hamstring(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Hamstring'


class Hit(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Hit'


class Impale(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Impale'


class Rip(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Rip'


class Ripost(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Ripost'


class Rush(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Rush'


class SavageLeap(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Savage Leap'


class SeverArtery(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Sever Artery'


class Swing(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Swing'


class Slash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Slash'


class Slice(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Slice'


class Gash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Gash'


class WildSlash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Wild Slash'


class Strike(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Strike'


class WildStrike(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Wild Strike'


class WildSwing(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Wild Swing'


class Smack(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Smack'


class Blow(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Blow'


class SkullCrack(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Skull Crack'


class WildBlow(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Wild Blow'


class Thrust(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Thrust'


class Jab(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Jab'


class WildThrust(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Wild Thrust'


class Advance(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Advance'


class Chop(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Chop'


class DoubleChop(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'DoubleChop'


class TripleChop(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Triple Chop'


class Cut(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Cut'


class Flurry(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Flurry'


class Whirl(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Whirl'


class WildBash(Ability):
    def __init__(self):
        Ability.__init__(self)
        self._name = 'Wild Bash'
