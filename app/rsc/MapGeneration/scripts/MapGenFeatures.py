#!/usr/bin/python

from MapGen import MapGen
import yaml
import re
from PIL import Image  # sudo pip install Pillow
from os import listdir
from os.path import isfile, join


class MapGenFeatures(MapGen):
    def __init__(self):
        MapGen.__init__(self)
        self._files_path = '../PNG/'
        self._map_type_derived = ['base', 'noise_z']
        self._map_type_new = 'feature'

    def generate_maps(self):
        maze_combos = []

        map_count = 1
        m1 = 0
        for maze_1 in self._maps['noise_z']:
            m2 = 0
            for maze_2 in self._maps['noise_z']:
                combo = str(m1) + ',' + str(m2)
                rcombo = str(m2) + ',' + str(m1)
            
                if maze_1 == maze_2 or combo in maze_combos or rcombo in maze_combos:
                    continue
                else:
                    for base_map in self._maps['base']:
                        for flora in self._flora_types:
                            input_maps = {
                                    'base': base_map,
                                    'maze_1': maze_1,
                                    'maze_2': maze_2,
                                }
                            self.generate_map(map_count, input_maps, flora)
                            map_count += 1

                maze_combos.append(combo)
                m2 += 1
            m1 += 1

    def generate_map(self, map_number, input_maps, variable):
        width = self._map_size
        height = self._map_size
        mid = 127

        new_map = Image.new('RGBA', (width, height))

        image_base = Image.open(self._files_path + input_maps['base'])
        pixel_base = image_base.load()

        image_maze_1 = Image.open(self._files_path + input_maps['maze_1'])
        pixel_maze_1 = image_maze_1.load()

        image_maze_2 = Image.open(self._files_path + input_maps['maze_2'])
        pixel_maze_2 = image_maze_2.load()

        flora_1 = self._dists[variable]['flora_1']
        flora_2 = self._dists[variable]['flora_2']
        flora_3 = self._dists[variable]['flora_3']
        flora_4 = self._dists[variable]['flora_4']
        flora_5 = self._dists[variable]['flora_5']
        water_1 = self._dists[variable]['water_1']
        water_2 = self._dists[variable]['water_2']
        spike_1 = self._dists[variable]['spike_1']
        spike_2 = self._dists[variable]['spike_2']
        spike_3 = self._dists[variable]['spike_3']
        spike_4 = self._dists[variable]['spike_4']
        spike_5 = self._dists[variable]['spike_5']
        flora_key_1 = self._feature_keys['flora_1']
        flora_key_2 = self._feature_keys['flora_2']
        flora_key_3 = self._feature_keys['flora_3']
        flora_key_4 = self._feature_keys['flora_4']
        flora_key_5 = self._feature_keys['flora_5']
        water_key_1 = self._feature_keys['water_1']
        water_key_2 = self._feature_keys['water_2']

        for y in range(0, height):
            for x in range(0, width):
                r, g, b, a = pixel_base[x,y]
                m1 = pixel_maze_1[x,y][0]
                m2 = pixel_maze_2[x,y][0]
                new_r = 0
                new_g = 0
                new_b = 0
                new_a = 0

                if b > water_1:
                    if m1 > mid and m2 > mid:
                        new_b = water_key_1
                    else:
                        new_b = water_key_2
                elif b > water_2 and r > spike_1:
                    if m1 > mid and m2 > mid:
                        new_b = water_key_1
                    else:
                        new_b = water_key_2
                elif b > water_2 and r > spike_2:
                    if m1 > mid and m2 > mid:
                        new_b = water_key_2
                    else:
                        new_b = 0
                elif ((g > flora_1 and r > spike_2) or
                      (g > flora_2 and r > spike_1) or
                      (g > flora_3 and r > spike_1)):
                    if m1 > mid and m2 > mid:
                        new_g = flora_key_1
                    elif m1 > mid or m2 > mid:
                        new_g = flora_key_4
                    else:
                        new_g = flora_key_5
                elif ((g > flora_2 and r > spike_2) or
                      (g > flora_3 and r > spike_2)):
                    if m1 > mid and m2 > mid:
                        new_g = flora_key_2
                    elif m1 > mid or m2 > mid:
                        new_g = flora_key_4
                    else:
                        new_g = flora_key_5
                elif g > flora_3 and r > spike_3:
                    if m1 > mid and m2 > mid:
                        new_g = flora_key_3
                    elif m1 > mid or m2 > mid:
                        new_g = flora_key_4
                    else:
                        new_g = flora_key_5
                elif g > flora_4 and r > spike_4:
                    if m1 > mid and m2 > mid:
                        new_g = flora_key_4
                    else:
                        new_g = flora_key_5
                elif g > flora_5 and r > spike_5:
                    if m1 > mid and m2 > mid:
                        new_g = flora_key_5
                    else:
                        new_g = 0
                else:
                    new_g = 0
                    new_b = 0
                    new_r = 0

                new_a = a

                new_map.putpixel((x, y),(new_r, new_g, new_b, new_a))

        full_path = self.make_full_path(
                feature_type=variable,
                old_file_name=input_maps['base'],
                )
        
        new_map.save(full_path)
        

if __name__ == "__main__":
    app = MapGenFeatures()
    app.run()
