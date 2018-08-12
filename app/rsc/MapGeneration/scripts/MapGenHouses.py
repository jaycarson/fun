#!/usr/bin/python

from HexMath import HexMath
from HexMath import Hex
from HexMap import HexMap
from MapGen import MapGen
import yaml
from PIL import Image  # sudo pip install Pillow
from os import listdir
from os.path import isfile, join


class MapGenHouses(MapGen):
    def __init__(self):
        MapGen.__init__(self)
        self._map_type_derived = [
                'farm',
            ]
        self._map_type_new = 'house'

    def generate_maps(self):
        map_count = 1
        for terrain_map in self._maps['farm']:
            input_maps = {'farm': terrain_map}
            self.generate_map(map_count, input_maps)
            map_count += 1

    def generate_map(self, map_number, input_maps, variable=None):
        hex_map = HexMap()
        hex_map.deserialize(self._files_path + input_maps['farm'])

        points = self.get_points_to_consider(hex_map)

        self.place_houses(points, hex_map)

        full_path = self.make_full_path(
                    map_number,
                    old_file_name=input_maps['farm']
                )

        hex_map.serialize(full_path)

    def get_points_to_consider(self, hex_map):
        points_to_consider = []
        step = self._house_radius + 1
        start = -127 + 4 + self._farm_radius
        stop = 127 - self._farm_radius
        threshold = self._house_radius * 200

        for x in range(start, stop, step):
            for y in range(start, stop, step):
                z = -x -y

                if z < start or z > stop:
                    continue

                point = hex_map.get_hex(x, y)

                #if self.is_occupied(point, hex_map):
                #    continue

                variance = hex_map.get_variance(point, self._house_radius)

                if variance < threshold:
                    points_to_consider.append(point)
                
        return points_to_consider

    def is_occupied(self, center, hex_map):
        occupied = False

        points = hex_map.hex_spiral(center, self._house_radius + 2)

        for point in points:
            if point.get_r() > 0:
                occupied = True
                break

        return occupied

    def place_houses(self, points, hex_map):
        house_count = 1
        placed_houses = []
        for point in points:
            if self.is_occupied(point, hex_map):
                continue
            self.place_house(point, hex_map, 'grass', house_count)
            house_count += 1

    def get_house_type(self, point, hex_map):
        water_2_id = self._feature_keys['water_2']
        flora_4_id = self._feature_keys['flora_4']
        flora_5_id = self._feature_keys['flora_5']
        grass = 0
        water = 0
        house_type = None

        for ground_point in hex_map.hex_spiral(point, self._house_radius):
            g = ground_point.get_g()
            b = ground_point.get_b()
            
            if b > water_2_id:
                water += 1
            if flora_5_id <= g and g < flora_4_id:
                grass += 1

        if grass >= water:
            house_type = 'grass'
        elif water > 0:
            house_type = 'fish'

        return house_type

    def place_house(self, point, hex_map, house_type, house_count):
        if house_type is None:
            return

        house_radius = self._house_radius
        house_wall_id = self._structure_ids['house_wall']
        house_floor_id = self._structure_ids['house_floor']
        house_dist = self._structure_defaults['increment_pop_house']
        population_level = house_count * house_dist

        if house_type == 'water':
            flora_id = 0
        elif house_type == 'grass':
            flora_id = self._feature_keys['flora_5']
        else:
            flora_id = 0

        average = int(hex_map.get_area_average(point, house_radius))

        for ground_point in hex_map.hex_spiral(point, house_radius):
            ground_point.set_g(flora_id)
            ground_point.set_a(average)
            ground_point.set_r(population_level)

        for house_floor in hex_map.hex_spiral(point, house_radius):
            house_floor.set_b(house_floor_id['b'])
            house_floor.set_r(population_level)

        for wall in hex_map.hex_ring(point, house_radius):
            wall.set_b(house_wall_id['b'])
            wall.set_r(population_level)


if __name__ == "__main__":
    app = MapGenHouses()
    app.run()
