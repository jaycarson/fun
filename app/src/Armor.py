#!/usr/bin/python


class Armor(object):
    def __init__(self,
                 armor_type,
                 piece,
                 quality,
                 color,
                 skills,
                 stats,
                 armor_id,
                 ):
        self._armor_type = armor_type
        self._piece = piece
        self._quality = quality
        self._color = color
        self._required_skills = skills
        self._stats = stats
        self._id = armor_id

    def get_id(self):
        return self._id

    def get_armor_type(self):
        return self._armor_type

    def get_piece(self):
        return self._piece

    def get_quality(self):
        return self._quality

    def get_color(self):
        return self._color

    def get_required_skills(self):
        return self._required_skills

    def get_stats(self):
        return self._stats
