#!/usr/bin/python

from MapGen import MapGen
import yaml
from PIL import Image  # sudo pip install Pillow
from os import listdir
from os.path import isfile, join

import sys
sys.path.insert(0, '../../../src')

from HexMap import HexMap, Hex


class MapGenCastle(MapGen):
    def __init__(self):
        MapGen.__init__(self)
        self._map_type_derived = [
                'terrain',
            ]
        self._map_type_new = 'castle'

    def generate_maps(self):
        map_count = 1
        for terrain_map in self._maps['terrain']:
            input_maps = {'terrain': terrain_map}
            self.generate_map(map_count, input_maps)
            map_count += 1

    def generate_map(self, map_number, input_maps, variable=None):
        hex_map = HexMap()
        hex_map.deserialize(self._files_path + input_maps['terrain'])
        
        points = self.get_points_to_consider(hex_map)
        point = self.select_an_origin(points, hex_map)

        self.place_castle(point, hex_map)

        full_path = self.make_full_path(
                    map_number,
                    old_file_name=input_maps['terrain']
                )

        hex_map.serialize(full_path)

    def get_points_to_consider(self, hex_map):
        points = []
        total_dist = 32
        steps = 8
        dist = total_dist / steps

        for x in range(-steps, steps + 1):
            for y in range(-steps, steps + 1):
                points.append(hex_map.get_hex(x * dist, y * dist))

        return points

    def select_an_origin(self, points, hex_map):
        radius = self._castle_radius + self._castle_wall_width

        current_point = hex_map.get_hex(0, 0)
        current_variance = hex_map.get_variance(
                point=current_point, 
                radius=radius
            )

        for point in points:
            variance = hex_map.get_variance(
                    point=point,
                    radius=radius,
                )
            if variance < current_variance:
                current_variance = variance
                current_point = point

        return current_point

    def place_castle(self, point, hex_map):
        castle_radius = self._castle_radius
        wall_width = self._castle_wall_width
        full_radius = castle_radius + wall_width
        castle_floor = self._structure_ids['castle_floor']
        castle_wall = self._structure_ids['castle_wall']

        average = int(hex_map.get_area_average(point, full_radius))

        castle_hexes = hex_map.spiral(point, castle_radius)

        for ground_point in hex_map.spiral(point, full_radius):
            ground_point.a = average

        for floor in hex_map.spiral(point, castle_radius):
            floor.r = castle_floor['r']
            floor.b = castle_floor['b']

        for ring in range(0, wall_width):
            walls = hex_map.ring(point, castle_radius + ring)
            for wall in walls:
                wall.r = castle_wall['r']
                wall.b = castle_wall['b']

        for ring in range(0, wall_width):
            outer_wall_radius = castle_radius * 3 + ring
            walls = hex_map.ring(point, outer_wall_radius)
            for wall in walls:
                wall.r = castle_wall['r']
                wall.b = castle_wall['b']


if __name__ == "__main__":
    app = MapGenCastle()
    app.run()
