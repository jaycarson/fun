#!/usr/bin/python

from HexMath import HexMath
from HexMath import Hex

import yaml
import re

from PIL import Image  # sudo pip install Pillow
from os import listdir
from os.path import isfile, join


class MapGen(object):
    def __init__(self):
        self._maps = {}
        self._files_path = '../PNG/'
        self._map_size = 256
        self._height = self._map_size
        self._width = self._map_size
        self._map_type_derived = []
        self._map_type_new = ''
        self._hex_math = HexMath()
        
        path = "../../Books/Geography.yml"
        self._book = yaml.load(open(path))
        self._terrain_types = self._book['types']
        self._flora_types = self._book['flora']
        self._dists = self._book['dists']
        self._feature_keys = self._book['feature_keys']
        
        structure_path = "../../Books/Structures.yml"
        self._structures_book = yaml.load(open(structure_path))
        self._structure_defaults = self._structures_book['defaults']
        self._structure_ids = self._structures_book['id_keys']
        self._castle_radius = self._structure_defaults['castle_radius']
        self._castle_wall_width = self._structure_defaults['castle_wall_width']
        self._zone_radius = self._structure_defaults['zone_radius']
        self._farm_radius = self._structure_defaults['farm_radius']
        self._house_radius = self._structure_defaults['house_radius']
        self._map_image_width = self._structure_defaults['map_image_width']
        self._map_image_height = self._structure_defaults['map_image_height']
        self._map_image_center_x = self._map_image_width / 2
        self._map_image_center_y = self._map_image_height / 2

    def run(self):
        print "MapGen: Running"

        for map_type in self._map_type_derived:
            self.collect_maps(map_type)

        self.generate_maps()

    def collect_maps(self, test_string=None):
        print "MapGen: Collecting Maps"

        test_string_name = test_string

        if test_string is None:
            test_string = self._map_type_derived

        collected_maps = []

        for map_file in listdir(self._files_path):
            if isfile(join(self._files_path, map_file)):
                if test_string in map_file:
                    collected_maps.append(map_file)

        self._maps[test_string_name] = collected_maps

    def generate_maps(self):
        print "MapGen: generate_maps: This method should have been overridden."
        return

    def generate_map(self, map_number, input_maps, variable=None):
        print "MapGen: generate_map: This method should have been overridden."
        return

    def make_full_path(
                self,
                map_number=0,
                old_file_name='',
                feature_type='',
                terrain_type='',
            ):

        if old_file_name != '':
            map_number = re.findall('\d+', old_file_name)[1]

        if map_number < 10:
            zeroes = '000'
        elif map_number < 100:
            zeroes = '00'
        elif map_number < 1000:
            zeroes = '0'
        else:
            zeroes = ''

        if old_file_name != '':
            for feature in self._flora_types:
                if feature in old_file_name:
                    feature_type = feature
            for terrain in self._terrain_types:
                if terrain in old_file_name:
                    terrain_type = terrain

        if feature_type != '':
            spaces = 11 - len(feature_type)
            for space in range(0, spaces):
                feature_type = feature_type + '_'

        if terrain_type != '':
            spaces = 9 - len(terrain_type)
            for space in range(0, spaces):
                terrain_type = terrain_type + '_'

        map_size = str(self._map_size) + '_'
        map_number = str(map_number) + '_'

        full_path = (
                self._files_path +
                self._map_type_new + '_' +
                map_size +
                zeroes +
                map_number +
                feature_type +
                terrain_type +
                '.png'
            )

        print "Generating: " + full_path

        return full_path

    def read_in_terrain(self, pixel_file):
        map_details = {}
        water_level = self._feature_keys['water_2']

        for y in range(0, self._height):
            for x in range(0, self._width):
                r, g, b, height = pixel_file[x,y]

                if b >= water_level:
                    has_water = True
                else:
                    has_water = False

                map_details[tuple(x, y)] = {
                        'height': height,
                        'has_water': has_water,
                        'structure': None,
                        'x': x,
                        'y': y,
                        'r': r,
                        'g': g,
                        'b': b,
                    }

        return map_details


if __name__ == "__main__":
    app = MapGen()
    app.run()
