#!/usr/bin/python

from PIL import Image  # sudo pip install Pillow


class MapMaker(object):
    def __init__(self, import_path, export_path):
        location_river = import_path + "r.png"
        location_mount = import_path + "m.png"
        location_flora = import_path + "f.png"
        location_humid = import_path + "h.png"
        location_ocean = import_path + "o.png"
        location_climate = import_path + "c.png"

        self._image_river = Image.open(location_river)
        self._pixel_river = self._image_river.load()
        
        self._image_mount = Image.open(location_mount)
        self._pixel_mount = self._image_mount.load()
        
        self._image_flora = Image.open(location_flora)
        self._pixel_flora = self._image_flora.load()
        
        self._image_humid = Image.open(location_humid)
        self._pixel_humid = self._image_humid.load()
        
        self._image_ocean = Image.open(location_ocean)
        self._pixel_ocean = self._image_ocean.load()
        
        self._image_climate = Image.open(location_climate)
        self._pixel_climate = self._image_climate.load()
        
        self._export_location = export_path
        self._game_map = {}
        self._rivers = {}
        #self.width = 128
        #self.height = 128
        self.width = 2048
        self.height = 2048

        self._terrain_types = {
            'Flat': 60,
            'Rough': 90,
            'Mesa': 120,
            'Mountain': 120,
            'Volcano': 150,
        }

        self._flora_types = {
            'Ocean': 0,
            'Wasteland': 20,
            'Desert': 40,
            'Tundra': 60,
            'Shrubland': 80,
            'Plain': 100,
            'Coniferous': 120,
            'Deciduous': 140,
            'Rainforest': 160,
            'Bog': 180,
            'Marsh': 200,
            'Swamp': 220,
            'Mangrove': 240,
        }

    def get_ocean(self, x, y):
        r, g, b, a = self._pixel_ocean[x,y]

        average = (r+g+b)/3
        
        percent = average / 255
        
        if percent < 0.3:
            return 'Ocean'
        elif percent < 0.31:
            return 'Mangrove'
        else:
            return 'Land'

    def get_climate(self, x, y):
        r, g, b, a = self._pixel_climate[x,y]

        average = (r+g+b)/3
        if average < 100:
            return 'Tropical'
        elif average < 200:
            return 'Temperate'
        else:
            return 'Arctic'

    def get_humidity(self, x, y):
        r, g, b, a = self._pixel_climate[x,y]
        average = (r+g+b)/3
        percent = average / 255
        humidity = 'Dry'

        if percent < 0.05:
            humidity = 'River Source'
        if percent < 0.33:
            humidity = 'Very Wet'
        if percent < 0.40:
            humidity = 'Wet'
        elif percent < 0.66:
            humidity = 'Averge'
        elif perfent = 'Dry'
        else:
            humidity = 'Very Dry'

        return humidity


    def get_flora(self, x, y):
        r, g, b, a = self._pixel_flora[x,y]

        ocean = self.get_ocean(x, y)

        if ocean == 'Ocean':
            return 'Ocean'
        elif ocean == 'Mangrove':
            flora = 'Mangrove'

        average = (r+g+b)/3
        flora_percent = average / 255
        flora = ''
        climate = self.get_climate(x, y)
        humidity = self.get_humidity(x, y)

        if climate == 'Tropical':
            if flora_percent < 0.5:
                if humidity == 'River Source':
                    flora = 'Rainforest'
                elif humidity == 'Very Wet':
                    flora = 'Rainforest'
                elif humidity == 'Wet':
                    flora = 'Deciduous'
                elif humidity == 'Average'
                    flora = 'Coniferous'
                elif humidity == 'Dry':
                    flora = 'Shrubland'
                elif humidity == 'Very Dry':
                    flora = 'Shrubland'
                else:
                    flora = 'Shrubland'
            else:
                if humidity == 'River Source':
                    flora = 'Bog'
                elif humidity == 'Very Wet':
                    flora = 'Marsh'
                elif humidity == 'Wet':
                    flora = 'Marsh'
                elif humidity == 'Average'
                    flora = 'Plains'
                elif humidity == 'Dry':
                    flora = 'Wasteland'
                elif humidity == 'Very Dry':
                    flora = 'Desert'
                else:
                    flora = 'Desert'
        elif climate == 'Temperate': 
            if flora_percent < 0.6:
                if humidity == 'River Source':
                    flora = 'Swamp'
                elif humidity == 'Very Wet':
                    flora = 'Coniferous'
                elif humidity == 'Wet':
                    flora = 'Deciduous'
                elif humidity == 'Average'
                    flora = 'Deciduous'
                elif humidity == 'Dry':
                    flora = 'Shrubland'
                elif humidity == 'Very Dry':
                    flora = 'Shrubland'
                else:
                    flora = 'Shrubland'
            else:
                if humidity == 'River Source':
                    flora = 'Bog'
                elif humidity == 'Very Wet':
                    flora = 'Marsh'
                elif humidity == 'Wet':
                    flora = 'Marsh'
                elif humidity == 'Average'
                    flora = 'Plains'
                elif humidity == 'Dry':
                    flora = 'Plains'
                elif humidity == 'Very Dry':
                    flora = 'Wasteland'
                else:
                    flora = 'Wasteland'
        elif climate == 'Arctic': 
            if flora_percent < 0.4:
                if humidity == 'River Source':
                    flora = 'Swamp'
                elif humidity == 'Very Wet':
                    flora = 'Coniferous'
                elif humidity == 'Wet':
                    flora = 'Coniferous'
                elif humidity == 'Average'
                    flora = 'Coniferous'
                elif humidity == 'Dry':
                    flora = 'Shrubland'
                elif humidity == 'Very Dry':
                    flora = 'Shrubland'
                else:
                    flora = 'Shrubland'
            else:
                if humidity == 'River Source':
                    flora = 'Bog'
                elif humidity == 'Very Wet':
                    flora = 'Marsh'
                elif humidity == 'Wet':
                    flora = 'Plains'
                elif humidity == 'Average'
                    flora = 'Tundra'
                elif humidity == 'Dry':
                    flora = 'Tundra'
                elif humidity == 'Very Dry':
                    flora = 'Wasteland'
                else:
                    flora = 'Wasteland'
        
        return flora

    def get_terrain(self, x, y):
        # To do: figure out what a river tile should be. Maybe
        # what is mostly around it?

        # Also, figure out which sides should have river sides
        # N  => Terrain +=  1
        # NE => Terrain +=  2
        # NW => Terrain +=  4
        # S  => Terrain +=  8
        # SE => Terrain += 16
        # SW => Terrain += 32
        # Lake => Terrain += 64
        r, g, b, a = self._pixel_mount[x,y]
        average = (r+g+b)/3
        percent = average/255

        terrain = 'Flat'

        if percent < 0.50:
            terrain = 'Flat'
        elif percent < 0.70:
            terrain = 'Hill'
        elif percent < 0.98:
            terrain = 'Mountain'
        else:
            terrain = 'Volcano'
        
        return terrain

    def has_river(self, x, y):
        r, g, b, a = self._pixel_river[x,y]
        average = (r+g+b)/3
        percent = average/255

        if percent > 0.5:
            return True
        else:
            return False

    def _land_by_river(self, x, y):
        n = self.get_pixel_alpha( x+0, y-1 )
        e = self.get_pixel_alpha( x+1, y+0 )
        w = self.get_pixel_alpha( x-1, y+0 )
        s = self.get_pixel_alpha( x+0, y+1 )
        ne = self.get_pixel_alpha( x+1, y-1 )
        nw = self.get_pixel_alpha( x-1, y-1 )
        se = self.get_pixel_alpha( x+1, y+1 )
        sw = self.get_pixel_alpha( x-1, y+1 )
        
        average = (n + s + e + w + ne + nw + se + sw)

        return average

    def _add_river(self, x, y):
        if self._has_river(x+1, y+0):
            self._rivers[(x+0, y+0)] = {'N': True}
            self._rivers[(x+1, y+0)] = {'NW': True}
            self._rivers[(x+0, y+1)] = {'S': True, 'SE': True}
        
        if self._has_river(x+0, y+1):
            self._rivers[(x+0, y+0)] = {'NW': True}
            self._rivers[(x+0, y+1)] = {'SW': True}
            self._rivers[(x-1, y+1)] = {'SE': True, 'NE': True}
        
        if self._has_river(x-1, y+0):
            self._rivers[(x+0, y+0)] = {'NW': True}
            self._rivers[(x-1, y+0)] = {'N': True}
            self._rivers[(x-1, y+1)] = {'SE': True, 'S': True}
        
        if self._has_river(x+0, y-1):
            self._rivers[(x+0, y+0)] = {'SW': True}
            self._rivers[(x+0, y-1)] = {'NW': True}
            self._rivers[(x-1, y+0)] = {'NE': True, 'SE': True}
        
        if self._has_river(x-1, y+1):
            self._rivers[(x+0, y+0)] = {'N': True}
            self._rivers[(x-1, y+1)] = {'NE': True}
            self._rivers[(x+0, y+1)] = {'S': True, 'SW': True}
        
        if self._has_river(x+1, y-1):
            self._rivers[(x+0, y+0)] = {'NE': True}
            self._rivers[(x+1, y-1)] = {'N': True}
            self._rivers[(x+1, y+0)] = {'SW': True, 'S': True}
        
    def get_pixel_alpha(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.width:
            return 0

        r, g, b, a = self._flora_pixel[x,y]

        return a

    def read_pixel(self, x, y):
        r, g, b, a = self._flora_pixel[x,y]

        self._game_map[(x, y)] = {
            'flora': self.get_flora(r, g, b),
            'terrain': self.get_terrain(a, x, y)
        }

    def run(self):
        self.count = 0
        print "Reading Map"

        for y in range(0, self.height):
            for x in range(0, self.width):
                self.read_pixel(x, y)
            print "    Read Row: " + str(y)
        print "Unknown: " + str(self.count)

        self.export_map()

    def export_map(self):
        # Final tuple for terrain to color =>
        #   ( Red,          Green,      Blue,        Alpha )
        #   ( Terrain Type, Flora Type, River/Lakes, Unk   )

        # Alpha is maybe temperature or moisture?

        print "Exporting Map"

        new_map = Image.new('RGBA', (self.width, self.height))

        for y in range(0, self.height):
            for x in range(0, self.width):
                flora_type = self._game_map[(x, y)]['flora']
                terrain_type = self._game_map[(x, y)]['terrain']
                water_type = self._get_water_type(x, y)
                new_map.putpixel(
                    (x, y),
                    (
                        terrain_type,
                        flora_type,
                        water_type,
                        255
                    )
                )
            print "    Export Row: " + str(y)

        new_map.save(self._export_location)

    def _get_water_type(self, x, y):
        water_type = 0
        if 'N' in self._rivers[(x, y)]:
            water_type += 1
        if 'NE' in self._rivers[(x, y)]:
            water_type += 2
        if 'SE' in self._rivers[(x, y)]:
            water_type += 4
        if 'NW' in self._rivers[(x, y)]:
            water_type += 8
        if 'SW' in self._rivers[(x, y)]:
            water_type += 16
        if 'S' in self._rivers[(x, y)]:
            water_type += 32
        if 'Lake' in self._rivers[(x, y)]:
            water_type += 64

        return water_type

if __name__ == "__main__":
    import_path = '../PNG/Map_000'
    export_path = '../PNG/MapFinal_000.png'
    generator = MapMaker(import_path=import_path, export_path=export_path)
    generator.run()
