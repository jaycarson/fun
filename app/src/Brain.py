#!/usr/bin/python

from random import choice


class Brains(object):
    def __init__(self):
        self.brains = {
                'meleedamage': BrainMeleeDamage(),
                'meleehealer': BrainMeleeHealer(),
                'meleetank': BrainMeleeTank(),
                'rangedamage': BrainRangeDamage(),
                'rangehealer': BrainRangeHealer(),
                'rangetank': BrainRangeTank(),
            }

    def __getitem__(self, item):
        return self.brains[item]


class Brain(object):
    def __init__(self):
        return

    def act(self, actor):
        self.find_target(actor)

        dm = actor.dm
        target = actor.target_enemy
        primary_attack = 0

        if target is None:
            return
        elif actor.get_range(primary_attack) >= dm.distance(actor, target):
            self.attack(actor, target, moved=False)
        else:
            self.move_towards(actor, target)
            self.attack(actor, target, moved=True)

    def find_target(self, actor):
        if actor.get_range(0) == 1:
            target = self.find_target_for_melee(actor)
        else:
            target = self.find_target_for_range(actor)
        
    def find_target_for_melee(self, actor):
        self.find_nearest_enemy(actor)

    def find_target_for_range(self, actor):
        self.find_nearest_enemy(actor)

    def find_nearest_enemy(self, actor):
        adjacent_enemies = actor.dm.get_adjacent_enemies(actor)

        if len(adjacent_enemies) > 0:
            actor.target_enemy = choice(adjacent_enemies)
        else:
            actor.target_enemy = actor.dm.get_nearest_enemy(actor)

    def attack(self, actor, target, moved):
        best = -1
        best_slot = 0
        distance = actor.dm.distance(actor, target)

        for slot in range(0, 5):
            current = actor.attack_hyp(
                    slot=slot,
                    distance=distance,
                    moved=moved,
                )
            if current > best:
                best = current
                best_slot = slot

        if best >= 0:
            actor.attack(
                    slot=best_slot,
                    distance=distance,
                )

    def move_towards(self, actor, target):
        actor.dm.move_char_along_path(
                actor=actor,
                source=actor.dungeon_hex,
                dest=target.dungeon_hex,
                distance=actor.movement,
            )
        actor.take_gcd(actor.movement_speed)


class BrainMeleeDamage(Brain):
    def __init__(self):
        Brain.__init__(self)


class BrainMeleeHealer(Brain):
    def __init__(self):
        Brain.__init__(self)


class BrainMeleeTank(Brain):
    def __init__(self):
        Brain.__init__(self)


class BrainRangeDamage(Brain):
    def __init__(self):
        Brain.__init__(self)


class BrainRangeHealer(Brain):
    def __init__(self):
        Brain.__init__(self)


class BrainRangeTank(Brain):
    def __init__(self):
        Brain.__init__(self)
