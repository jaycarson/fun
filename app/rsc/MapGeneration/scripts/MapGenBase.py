#!/usr/bin/python

from MapGen import MapGen
import yaml
from PIL import Image  # sudo pip install Pillow
from os import listdir
from os.path import isfile, join


class MapGenBase(MapGen):
    def __init__(self):
        MapGen.__init__(self)
        self._files_path = '../PNG/'
        self._map_type_derived = ['noise_o', 'noise_t']
        self._map_type_new = 'base'

    def generate_maps(self):
        print "MapGenBase: Generating Maps"
        map_count = 1

        for flora_map in self._maps['noise_o']:
            for water_map in self._maps['noise_o']:
                for height_map in self._maps['noise_o']:
                    if(
                        flora_map == water_map or
                        flora_map == height_map or
                        water_map == height_map
                        ):
                        continue
                    else:
                        for heat_map in self._maps['noise_t']:
                            input_maps = {
                                'heat': heat_map,
                                'flora': flora_map,
                                'water': water_map,
                                'height': height_map,
                                }
                            self.generate_map(
                                map_number=map_count,
                                input_maps=input_maps
                                )

                            map_count += 1

    def generate_map(self, map_number, input_maps):
        width = self._map_size
        height = self._map_size

        new_map = Image.new('RGBA', (width, height))

        image_heat = Image.open(self._files_path + input_maps['heat'])
        pixel_heat = image_heat.load()

        image_flora = Image.open(self._files_path + input_maps['flora'])
        pixel_flora = image_flora.load()

        image_water = Image.open(self._files_path + input_maps['water'])
        pixel_water = image_water.load()

        image_height = Image.open(self._files_path + input_maps['height'])
        pixel_height = image_height.load()

        for y in range(0, height):
            for x in range(0, width):
                heat_r, g, b, a = pixel_heat[x,y]
                r, flora_g, b, a = pixel_flora[x,y]
                r, g, water_b, a = pixel_water[x,y]
                height_a, g, b, a = pixel_height[x,y]
                new_map.putpixel(
                    (x, y),
                    (
                        heat_r,
                        flora_g,
                        water_b,
                        height_a,
                    )
                )

        full_path = self.make_full_path(map_number=map_number)
        
        new_map.save(full_path)
        

if __name__ == "__main__":
    app = MapGenBase()
    app.run()
