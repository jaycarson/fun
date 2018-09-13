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
                 dice,
                 ):
        self.armor_type = armor_type
        self.piece = piece
        self.quality = quality
        self.color = color
        self.required_skills = skills
        self.stats = stats
        self.id = armor_id
        self.dice = dice

    def get_stat(self, stat):
        assert stat in self.stats
        return self.stats.get(stat)

    def roll_dice(self):
        return self.dice.roll()

    def get_dice_face(self):
        return self.dice.get_value()

    def set_dice_face(self, face):
        self.dice.value = face
