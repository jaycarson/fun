#!/usr/bin/python

from MapGen import MapGen
import yaml
from PIL import Image  # sudo pip install Pillow
from os import listdir
from os.path import isfile, join

import sys
sys.path.insert(0, '../../../src')

from HexMap import HexMap, Hex


class MapGenFarms(MapGen):
    def __init__(self):
        MapGen.__init__(self)
        self._map_type_derived = [
                'castle',
            ]
        self._map_type_new = 'farm'

    def generate_maps(self):
        map_count = 1
        for terrain_map in self._maps['castle']:
            input_maps = {'castle': terrain_map}
            self.generate_map(map_count, input_maps)
            map_count += 1

    def generate_map(self, map_number, input_maps, variable=None):
        hex_map = HexMap()
        hex_map.deserialize(self._files_path + input_maps['castle'])

        points = self.get_points_to_consider(hex_map)

        self.place_farms(points, hex_map)

        full_path = self.make_full_path(
                    map_number,
                    old_file_name=input_maps['castle']
                )

        hex_map.serialize(full_path)

    def get_points_to_consider(self, hex_map):
        points_to_consider = []

        points = hex_map.ring(
                hex_map.get_hex(0, 0),
                self._zone_radius - 20
            )

        for point in points:
            if 100000 < hex_map.get_variance(point, self._farm_radius):
                continue

            points_to_consider.append(point)
        
        return points_to_consider

    def place_farms(self, points, hex_map):
        placed_farms = []
        farm_count = 1
        for point in points:
            if self.farm_is_remote(point, placed_farms, hex_map):
                farm_type = self.get_farm_type(point, hex_map)
                self.place_farm(point, hex_map, farm_type, farm_count)
                farm_count += 1

    def farm_is_remote(self, point, placed_farms, hex_map):
        arbitrary = 4
        remoteness = self._farm_radius * arbitrary

        for farm in placed_farms:
            distance = hex_map.distance(point, farm)
            if distance < remoteness:
                return False

        placed_farms.append(point)
        return True

    def get_farm_type(self, point, hex_map):
        water_2_id = self._feature_keys['water_2']
        flora_4_id = self._feature_keys['flora_4']
        flora_5_id = self._feature_keys['flora_5']
        grass = 0
        water = 0
        farm_type = None

        for ground_point in hex_map.spiral(point, self._farm_radius):
            if ground_point.b > water_2_id:
                water += 1
            if flora_5_id <= ground_point.g and ground_point.g < flora_4_id:
                grass += 1

        if grass >= water:
            farm_type = 'grass'
        elif water > 0:
            farm_type = 'fish'

        return farm_type

    def place_farm(self, point, hex_map, farm_type, farm_count):
        if farm_type is None:
            return

        farm_radius = self._farm_radius
        house_radius = self._house_radius
        house_wall = self._structure_ids['house_wall']
        house_floor = self._structure_ids['house_floor']
        ground_farm = self._structure_ids['ground_farm']
        farm_dist = self._structure_defaults['increment_pop_farm']
        population_level = farm_count * farm_dist
        
        if farm_type == 'fish':
            water_id = self._feature_keys['water_2']
            flora_id = 0
        elif farm_type == 'grass':
            water_id = 0
            flora_id = self._feature_keys['flora_5']
        else:
            water_id = 0
            flora_id = 0

        average = int(hex_map.get_area_average(point, farm_radius))

        for ground_point in hex_map.spiral(point, farm_radius):
            ground_point.g = flora_id
            ground_point.b = ground_farm['b']
            ground_point.a = average
            ground_point.r = population_level

        for farm_floor in hex_map.spiral(point, house_radius):
            farm_floor.b = house_floor['b']
            farm_floor.r = population_level

        for wall in hex_map.ring(point, house_radius):
            wall.b = house_wall['b']
            wall.r = population_level


if __name__ == "__main__":
    app = MapGenFarms()
    app.run()
