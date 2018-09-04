#!/usr/bin/python

import random


class Brains(object):
    def __init__(self):
        self.brains = {
                'meleedamage': Brain(),
                'meleehealer': Brain(),
                'meleetank': Brain(),
                'rangedamage': Brain(),
                'rangehealer': Brain(),
                'rangetank': Brain(),
            }

    def __getitem__(self, item):
        return self.brains[item]


class Brain(object):
    def __init__(self):
        return

    def act(self, actor):
        
        
        return


class BrainMelee(Brain):
    def __init__(self):
        Brain.__init(self)


class BrainRange(Brain):
    def __init__(self):
        Brain.__init(self)


class BrainHealer(Brain):
    def __init__(self):
        Brain.__init(self)


class BrainTank(Brain):
    def __init__(self):
        Brain.__init(self)
