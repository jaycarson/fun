#!/usr/bin/python

from Library import BookGeography

from random import seed
from PIL import Image  # sudo pip install Pillow


class Geography(object):
    def __init__(self,
                 geo_id=0):
        self._node_map = {}
        self._geo_id = geo_id

        self._terrain = ''
        self._flora = ''
        self._book_geography = BookGeography()

        seed(geo_id)

        self._define_node_properties()
        self._generate_node_map()

    def set_terrain(self, terrain):
        self._terrain = terrain

    def set_flora(self, flora):
        self._flora = flora

    def get_terrain(self):
        return self._terrain

    def get_flora(self):
        return self._flora

    def _generate_node_map(self):
        np = self._node_properties

        for x in range(-radius, radius):
            for y in range(max(-radius, -x-radius), min(+radius, -x+radius):
                z = -x-y
                self._node_map[tuple(x, y, z)] = self.read_map_location(x, y)
    
    def read_map(self, x, y):
        r, g, b, a = self._map[x,y]
        return self.interpret(r=r, g=g, b=b, a=a)

    def _load_map_file(self, path):
        self._map = Image.open(path)
        self._map = self._map.load()

    def interpret(r, g, b, a):
        return

    def define_node_properties(self):
        return


class Locale(Geography):
    def __init__(self,
                 geo_id=0):
        Geography.__init__(self, geo_id=geo_id)

    def interpret(r, g, b, a):
        data = {}
        
        data['height'] = int(a/256*20-10)

        if g > self.dist['big_flora']:
            data['feature'] = self.feature['flora_heavy']
        elif b > self.dist['wet_heavy']:
            data['feature'] = self.feature['wet_heavy']
        elif b > self.dist['wet_light']:
            data['feature'] = self.feature['wet_light']
        elif g > self.dist['flora_light'] and b > self.dist['wet_light']:
            data['feature'] = self.feature['wet_flora']
        elif g > self.dist['flora_light']:
            data['feature'] = self.feature['flora_light']
        else:
            data['feature'] = self.feature['default']


        return data


class Region(Geography):
    def __init__(self,
                 geo_id=0):
        Geography.__init__(self, geo_id=geo_id)

    def interpret(r, g, b, a):
        return


class World(Geography):
    def __init__(self,
                 geo_id=0):
        Geography.__init__(self, geo_id=geo_id)

    def interpret(r, g, b, a):
        return
