#!/usr/bin/python

from MapGen import MapGen
import yaml
import re
from PIL import Image  # sudo pip install Pillow
from os import listdir
from os.path import isfile, join


class MapGenTerrain(MapGen):
    def __init__(self):
        MapGen.__init__(self)
        self._map_type_derived = [
                'feature',
                'noise_p',
                'noise_h',
                'noise_m',
            ]
        self._map_type_new = 'terrain'

    def generate_maps(self):
        map_count = 1
        for feature_map in self._maps['feature']:
            for terrain in self._terrain_types:
                terrain_map = None

                if terrain == 'plain':
                    terrain_map = self._maps['noise_p'][0]
                elif terrain == 'hill':
                    terrain_map = self._maps['noise_h'][0]
                elif terrain == 'mountain':
                    terrain_map = self._maps['noise_m'][0]

                if terrain_map is not None:
                    input_maps = {
                            'feature': feature_map,
                            'terrain': terrain_map,
                        }
                    self.generate_map(map_count, input_maps, terrain)
                    map_count += 1

    def generate_map(self, map_number, input_maps, terrain_type):
        width = self._map_size
        height = self._map_size

        new_map = Image.new('RGBA', (width, height))

        image_file = Image.open(self._files_path + input_maps['feature'])
        pixel_file = image_file.load()
        
        image_terrain = Image.open(self._files_path + input_maps['terrain'])
        pixel_terrain = image_terrain.load()
        
        for y in range(0, height):
            for x in range(0, width):
                r, g, b, a = pixel_file[x,y]
                t_height, t_g, t_b, t_a = pixel_terrain[x,y]

                g_ratio = g/255
                b_ratio = b/255

                new_r = r
                new_g = g
                new_b = b
                new_a = int(
                        (
                            (1-g_ratio)*a+g_ratio*t_height
                        )*(1-b_ratio)-r*(b_ratio)
                    )

                new_map.putpixel((x, y),(new_r, new_g, new_b, new_a))


        full_path = self.make_full_path(
                map_number,
                terrain_type=terrain_type,
                old_file_name=input_maps['feature'],
            )

        new_map.save(full_path)


if __name__ == "__main__":
    app = MapGenTerrain()
    app.run()
