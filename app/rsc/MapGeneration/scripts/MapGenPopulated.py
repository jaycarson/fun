#!/usr/bin/python

from HexMath import HexMath
from HexMath import Hex
import yaml
from PIL import Image  # sudo pip install Pillow
from os import listdir
from os.path import isfile, join


class MapGenPopulated(object):
    def __init__(MapGen):
        MapGen.__init__(self)
        self._map_type_derived = [
                'terrain',
            ]
        self._map_type_new = 'final'
        self._hex_math = HexMath()

        path = "../../Books/Structures.yml"
        self._structures_book = yaml.load(open(path))
        self._structure_defaults = self._structures_book['defaults']
        self._castle_radius = self._structure_defaults['castle_radius']
        self._castle_wall_width = self._structure_defaults['castle_wall_width']
        self._home_radius = self._structure_defaults['home_radius']
        self._home_wall_width = self._structure_defaults['home_wall_width']
        self._road_width = self._structure_defaults['road_width']
        self._zone_radius = self._structure_defaults['zone_radius']
        self._map_image_width = self._structure_defaults['map_image_width']
        self._map_image_height = self._structure_defaults['map_image_height']
        self._map_image_center_x = self._map_image_width / 2
        self._map_image_center_y = self._map_image_height / 2

    def generate_maps(self, map_set):
        map_count = 1
        for terrain_map in self._maps['terrain']:
            input_maps = {'terrain': terrain_map}
            self.generate_map(map_count, input_maps)
            map_count += 1

    def generate_map(self, map_number, input_maps, variable=None):
        width = self._map_size
        height = self._map_size

        new_map = Image.new('RGBA', (width, height))

        image_file = Image.open(self._files_path + input_maps['terrain'])
        pixel_file = image_file.load()

        map_details = self.read_in_terrain(pixel_file)
        self.place_castle(map_details)
        self.place_farms(map_details)
        self.place_houses(map_details)

    def read_in_terrain(self, pixel_file):
        map_details = {}
        water_level = self._feature_keys['water_2']

        for y in range(0, height):
            for x in range(0, width):
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

    def place_castle(self, map_details):
        center = self.find_castle_center(map_details)
        x = castle_center[0]
        y = castle_center[1]
        average = castle_center[2]

        castle_walls = []
        castle_floor = []

        for ring in range(0, self._castle_wall_width):
            radius = self._castle_radius + ring
            castle_walls += self._hex_math.hex_ring(x, y, radius)

        castle_floor = self._hex_math.hex_spiral(x, y, self._castle_radius)

        self.place(castle_walls, map_details, self._castle_wall_id)
        self.place(castle_floor, map_details, self._castle_floor_id)

    def find_castle_center(self, map_details):
        plots = {}
        x_start = self._map_image_width / 4
        x_end = self._map_image_width * 3 / 4
        y_start = self._map_image_height / 4
        y_end = self._map_image_height * 3 / 4
        radius = self._castle_radius + self._castle_wall_radius + 1

        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                variance, average = self.get_area_variance(
                                        x=x,
                                        y=y,
                                        radius=radius,
                                        map_details=map_details,
                                    )
                plots[tuple(x, y)] = {
                        'variance': variance,
                        'average': average,
                        'x': x,
                        'y': y,
                    }

        return self.get_smallest_variance(plots)

    def get_area_variance(self, x, y, radius, map_details):
        y_start = y - radius
        y_end = y + radius
        x_start = x - radius
        x_end = x + radius

        points = []
        sum_of_points = 0
        count_of_points = 0
        variance = 0
        invalidator = 1000000

        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                key = tuple(x, y)

                if key in map_details.keys():
                    if map_details[key]['structure'] is not None:
                        height = invalidator
                    else:
                        height = map_details[key]['height']
                else:
                    height = invalidator

                sum_of_points += height
                points.append(height)
                count_of_points += 1

        average = sum_of_points / count_of_points

        for point in points:
            variance = (
                    variance +
                    abs(point - average) * abs(point - average)
                )

        return [variance, average]

    def get_smallest_variance(self, plots):
        x_smallest = None
        y_smallest = None
        smallest = None
        average = None
        for key in plots.keys():
            if smallest is None:
                smallest = plots[key]['height']
                x_smallest = plot[key]['x']
                y_smallest = plot[key]['y']
                average = plots[key]['average']

            if plots[key]['height'] < smallest:
                smallest = plots[key]['height']
                x_smallest = plot[key]['x']
                y_smallest = plot[key]['y']
                average = plots[key]['average']

        point = [x, y, average]
        return point

    def place_farms(self, map_details):
        return

    def place_houses(self, map_details):
        return

    def place(self, hexes, map_details, structure_id):
        for _hex in hexes:
            x = _hex.get_x()
            y = _hex.get_y()
            map_details[tuple(x,y)]['structures'] = structure_id


if __name__ == "__main__":
    app = MapGenPopulated()
    app.run()
