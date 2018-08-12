#!/usr/bin/python

from Character import Character


class CharacterPC(object):
    def __init__(self, experience=0, race='human', name='None'):
        Character.__init__(
            self,
            experience=experience,
            race=race,
            name=name,
        )
