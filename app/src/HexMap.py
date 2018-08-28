#!/usr/bin/python

from PIL import Image  # sudo pip install Pillow


class Hex(object):
    def __init__(self, x, y, z=None):
        if z is None:
            z = -x -y

        self.x = x
        self.y = y
        self.z = z
        self.r = 0
        self.g = 0
        self.b = 0
        self.a = 0
        self.ground = 'grass'
        self.height = 10
        self.character = None

    def set_color(self, r=0, g=0, b=0, a=0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


class HexMap(object):
    def __init__(self):
        self.hex_map = {}
        self.image_width = 256
        self.image_height = 256
        self.map_radius = 127
        self.center_disp_x = self.image_width / 2
        self.center_disp_y = self.image_height / 2
        
        self.get_hex = self.get_hex_actual
        
        self.arena_height = 10
        self.arena_ground = 'grass'

        self.directions = [
                Hex(1, 0, -1), 
                Hex(1, -1, 0), 
                Hex(0, -1, 1), 
                Hex(-1, 0, 1), 
                Hex(-1, 1, 0), 
                Hex(0, 1, -1),
            ]
        
        self.diagonals = [
                Hex(2, -1, -1),
                Hex(1, -2, 1),
                Hex(-1, -1, 2),
                Hex(-2, 1, 1),
                Hex(-1, 2, -1),
                Hex(1, 1, -2),
            ]

    def set_image_dimenstions(self, x, y):
        self.image_width = x
        self.image_height = y

    def serialize(self, path):
        new_map = Image.new(
                'RGBA', 
                (self.image_width, self._image_height)
            )

        for key in self.hex_map.keys():
            this_hex = self.hex_map[key]
            x = this_hex.x + self.center_disp_x
            y = this_hex.y + self.center_disp_y
            r = this_hex.r
            g = this_hex.g
            b = this_hex.b
            a = this_hex.a

            new_map.putpixel(
                    (x, y),
                    (r, g, b, a)
                )

        new_map.save(path)

    def deserialize(self, path=None):
        if path is None:
            return

        image_map = Image.open(path)
        self.pixel_map = image_map.load()

        self.initialize_map()

    def initialize_map(self):
        self.get_hex = self.get_hex_initial
        self.hex_map = {}
        point = self.get_hex(x=0, y=0)
        self.spiral(center_hex=point, radius=self.map_radius)
        self.get_hex = self.get_hex_actual

    def get_hex_actual(self, x, y, z=None):
        if z is None:
            z = -x - y

        key = (x, y, z)
        
        return self.hex_map[key]

    def get_hex_initial(self, x, y, z=None):
        if z is None:
            z = -x - y

        key = (x, y, z)

        disp_x = x + self.center_disp_x
        disp_y = y + self.center_disp_y
        if (
            disp_x >= 0 and
            disp_y >= 0 and
            disp_x < self.image_width and
            disp_y < self.image_height
        ):
            r, g, b, a = self.pixel_map[disp_x, disp_y]
            new_hex = Hex(x, y, z)
            new_hex.set_color(r=r, g=g, b=b, a=a)
            self.hex_map[key] = new_hex
            
            return new_hex

    def get_hex_arena(self, x, y, z=None):
        if z is None:
            z = -x - y

        key = (x, y, z)

        new_hex = Hex(x, y, z)
        new_hex.ground = self.arena_ground
        new_hex.height = self.arena_height
        self.hex_map[key] = new_hex
            
        return new_hex

    def get_hypotheical_hex(self, x, y, z=0):
        return Hex(x, y, z)

    def add(self, hex_1, hex_2):
        return self.get_hex(
                hex_1.x + hex_2.x,
                hex_1.y + hex_2.y,
                hex_1.z + hex_2.z,
            )

    def subtract(self, hex_1, hex_2):
        return self.get_hypotheical_hex(
                hex_1.x - hex_2.x,
                hex_1.y - hex_2.y,
                hex_1.z - hex_2.z,
            )

    def scale(self, input_hex, scale):
        return self.get_hex(
                input_hex.x * scale,
                input_hex.y * scale,
                input_hex.z * scale,
            )

    def get_rotate_left(self, input_hex):
        return self.get_hex(
                x=-input_hex.z,
                y=-input_hex.x,
                z=-input_hex.y,
            )

    def get_rotate_right(self, input_hex):
        return self.get_hex(
                x=-input_hex.y,
                y=-input_hex.z,
                z=-input_hex.x,
            )

    def get_direction(self, direction):
        return self.directions[direction]

    def neighbor(self, input_hex, direction):
        return self.add(
                input_hex,
                self.get_direction(direction)
            )

    def neighbors(self, input_hex):
        neighbors = []
        for x in range(0, 6):
            neighbors.append(self.neighbor(input_hex, x))

        return neighbors

    def get_diagonal_neighbor(self, input_hex, direction):
        return add(
                input_hex,
                self.diagonals[direction]
            )

    def length(self, input_hex):
        hex_sum = (
                abs(input_hex.x) +
                abs(input_hex.y) +
                abs(input_hex.z)
            )
        return hex_sum // 2

    def distance(self, hex_1, hex_2):
        return self.length(self.subtract(hex_1, hex_2))

    def round(self, h):
        qi = int(round(h.q))
        ri = int(round(h.r))
        si = int(round(h.s))
        q_diff = abs(qi - h.q)
        r_diff = abs(ri - h.r)
        s_diff = abs(si - h.s)
        if q_diff > r_diff and q_diff > s_diff:
            qi = -ri - si
        else:
            if r_diff > s_diff:
                ri = -qi - si
            else:
                si = -qi - ri
        return Hex(qi, ri, si)

    def lerp(self, hex_1, hex_2, t):
        return self.get_hex(
                hex_1.x * (1 - t) + hex_2.x * t,
                hex_1.y * (1 - t) + hex_2.y * t,
                hex_1.z * (1 - t) + hex_2.z * t
            )

    def linedraw(self, hex_1, hex_2):
        dist = self.distance(hex_1, hex_2)
        
        hex_1_nudge = Hex(
                hex_1.x + 0.000001,
                hex_1.y + 0.000001,
                hex_1.z - 0.000002
            )

        hex_2_nudge = Hex(
                hex_2.x + 0.000001,
                hex_2.y + 0.000001,
                hex_2.z - 0.000002
            )

        results = []
        
        step = 1.0 / max(dist, 1)
        
        for i in range(0, dist + 1):
            results.append(
                    self.round(
                        self.lerp(
                            hex_1_nudge,
                            hex_2_nudge,
                            step * i,
                        )
                    )
                )

        return results

    def ring(self, center_hex, radius):
        results = []

        current_hex = self.add(
                        center_hex, 
                        self.scale(self.get_direction(4), radius)
                    )

        for direction in range(0, 6):
            for length in range(0, radius):
                results.append(current_hex)
                current_hex = self.neighbor(current_hex, direction)
        
        return results

    def spiral(self, center_hex, radius):
        results = [center_hex]

        for step in range(0, radius + 1):
            results += self.ring(
                    center_hex=center_hex,
                    radius=step,
                )

        return results

    def get_variance(self, point, radius):
        points = self.spiral(point, radius)
        
        total = 0
        count = 0
        variance = 0

        for tot_point in points:
            total += tot_point.a
            count += 1

        average = total/count

        for var_point in points:
            dif = var_point.a - average
            variance = variance + (dif * dif)

        return variance

    def get_area_average(self, point, radius):
        points = self.spiral(point, radius)
        
        total = 0
        count = 0

        for point in points:
            total += point.a
            count += 1

        average = total/count
        return average

    def create_arena(self, arena=None, radius=5):
        self.map_radius = radius
        self.get_hex = self.get_hex_arena
        self.arena_height = 10
        self.arena_ground = 'grass'

        self.hex_map = {}
        point = self.get_hex(x=0, y=0)
        self.spiral(center_hex=point, radius=self.map_radius)

        self.get_hex = self.get_hex_actual
