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
        self.armor_type = armor_type
        self.piece = piece
        self.quality = quality
        self.color = color
        self.required_skills = skills
        self.stats = stats
        self.id = armor_id
