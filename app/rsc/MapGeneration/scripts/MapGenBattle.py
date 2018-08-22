#!/usr/bin/python

from HexMath import HexMath
from HexMath import Hex
from MapGen import MapGen

import yaml
from PIL import Image  # sudo pip install Pillow
from os import listdir
from os.path import isfile, join


class MapGenBattle(MapGen):
    def __init__(self):
        MapGen.__init__(self)
        self._map_type_derived = [
                'house',
            ]
        self._map_type_new = 'battle'

        self._scaling = 8
        self._local_map_size = 256
        self._battle_map_size = 256 / self._scaling

    def generate_maps(self):
        map_count = 1
        for terrain_map in self._maps['house']:
            input_maps = {'house': terrain_map}
            self.generate_map(map_count, input_maps)
            map_count += 1

    def generate_map(self, map_number, input_maps, variable=None):
        local_map = HexMap()
        local_map.deserialize(self._files_path + input_maps['house'])

        full_path = self.make_full_path(
                    map_number,
                    old_file_name=input_maps['house']
                )

        battle_map = HexMap()
        battle_map.set_dimensions(
                x=self._battle_map_size,
                y=self._battle_map_size,
            )
        
        self.scale_maps(
                input_map=local_map,
                output_map=battle_map,
            )

        battle_map.serialize(full_path)

    def scale_maps(self, input_map, output_map):
        for y in range(0, output_map.get_height):
            for x in range(0, output_map.get_width):
                self.set_area_type(input_map, output_map, x, y)

    def set_area_type(self, input_map, output_map, x, y):
        scaling = int(input_map.get_size / input_map.get_size)
        scaling_radius = int(scaling / 2) - 1

        center = hex_map.get_hex(x * scaling, y * scaling)
        points = hex_map.hex_spiral(center, scaling_radius)

        counts = {
            'flora_1': 0,
            'flora_2': 0,
            'flora_3': 0,
            'flora_4': 0,
            'flora_6': 0,
            'water_1': 0,
            'water_2': 0,
            'castle_floor': 0,
            'castle_wall': 0,
            'castle_gate': 0,
            'house': 0,
            'house_water': 0,
            'farm': 0,
            'farm_water': 0,
        }

        ids = self._structure_ids

        for point in points:
            for count_id in counts.key():
                if (
                    point.get_r() >= ids[count_id]['r'] and
                    point.get_g() >= ids[count_id]['g'] and
                    point.get_b() >= ids[count_id]['b'] and
                    point.get_a() >= ids[count_id]['a']
                ):
                    current_count = counts[count_id]
                    counts[count_id] = current_count + 1

        max_id = ''
        max_count = 0

        for count_id in counts.keys():
            if counts[count_id] > max_count:
                max_count = counts[count_id]
                max_id = count_id

        output_map.set_r(ids[max_id]['r'])
        output_map.set_g(ids[max_id]['g'])
        output_map.set_b(ids[max_id]['b'])
        output_map.set_a(ids[max_id]['a'])
