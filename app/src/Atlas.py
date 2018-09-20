#!/usr/bin/python


class Atlas(object):
    def __init__(self, character_id, library):
        self.library = library
        self._owner = character_id
        self._atlas = {}
        self._book_atlas = self.library.get_book('atlas')

        self._terrain_types = self._book_atlas.get_terrain_types()
        self._flora_types = self._book_atlas.get_flora_types()
        self._tile_sides = self._book_atlas.get_tile_sides()

    def get_owner(self):
        return self._owner

    def add_locality(self, x, y, z, h, terrain_type, flora_type):
        if terrain_type not in self._terrain_types:
            terrain_type = 'Unknown'

        if flora_type not in self._flora_types:
            flora_type = 'Unkown'

        locality_info = {
            'terrain_type': terrain_type,
            'flora_type': flora_type,
            'owner_id': 'None',
            'river_n': False,
            'river_ne': False,
            'river_se': False,
            'river_s': False,
            'river_sw': False,
            'river_nw': False,
        }
        self._atlas[(x, y, z, h)] = locality_info

    def set_owner(self, x, y, z, y, owner_id):
        self._atlas[(x, y, z, h)]['owner_id'] = owner_id

    def change_flora_type(self, x, y, z, h, flora_type):
        self._atlas[(x, y, z, h)]['flora_type'] = flora_type

    def change_terrain_type(self, x, y, z, h, terrain_type):
        self._atlas[(x, y, z, h)]['terrain_type'] = terrain_type

    def get_locality_attribute(self, x, y, z, h, attribut):
        return self._atlas[(x, y, z, h)][attribute]

    def set_river(self, x, y, z, h, side):
        if side in self._tile_sides:
            tile_side = "river_" + side
            self._atlas[(x, y, z, h)][tile_side] = True
