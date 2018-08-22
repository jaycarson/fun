#!/usr/bin/python

from HexMath import Hex
from HexMath import HexMath
from PIL import Image  # sudo pip install Pillow


class HexMap(object):
    def __init__(self):
        self._hex_map = {}
        self._image_width = 256
        self._image_height = 256
        self._center_disp_x = self._image_width / 2
        self._center_disp_y = self._image_height / 2

        self._directions = [
                Hex(1, 0, -1), 
                Hex(1, -1, 0), 
                Hex(0, -1, 1), 
                Hex(-1, 0, 1), 
                Hex(-1, 1, 0), 
                Hex(0, 1, -1),
            ]
        
        self._diagonals = [
                Hex(2, -1, -1),
                Hex(1, -2, 1),
                Hex(-1, -1, 2),
                Hex(-2, 1, 1),
                Hex(-1, 2, -1),
                Hex(1, 1, -2),
            ]

    def set_dimenstions(self, x, y):
        self._image_width = x
        self._image_height = y

    def serialize(self, path):
        new_map = Image.new(
                'RGBA', 
                (self._image_width, self._image_height)
            )

        for key in self._hex_map.keys():
            this_hex = self._hex_map[key]
            x = this_hex.get_x() + self._center_disp_x
            y = this_hex.get_y() + self._center_disp_y
            r = this_hex.get_r()
            g = this_hex.get_g()
            b = this_hex.get_b()
            a = this_hex.get_a()

            new_map.putpixel(
                    (x, y),
                    (r, g, b, a)
                )

        new_map.save(path)

    def deserialize(self, path=None):
        if path is None:
            return

        image_map = Image.open(path)
        self._pixel_map = image_map.load()

        self.initialize_map()

    def initialize_map(self):
        self._initializing = True
        self._hex_map = {}
        point = self.get_hex(x=0, y=0)
        self.hex_spiral(center_hex=point, radius=127)
        self._initializing = False

    def get_hex(self, x, y, z=None):
        if z is None:
            z = -x - y

        key = (x, y, z)

        if not self._initializing:
            return self._hex_map[key]

        disp_x = x + self._center_disp_x
        disp_y = y + self._center_disp_y
        if (
            disp_x >= 0 and
            disp_y >= 0 and
            disp_x < self._image_width and
            disp_y < self._image_height
        ):
            r, g, b, a = self._pixel_map[disp_x, disp_y]
            new_hex = Hex(x, y, z)
            new_hex.set_color(r=r, g=g, b=b, a=a)
            self._hex_map[key] = new_hex
            
            return new_hex

    def get_hypotheical_hex(self, x, y, z=0):
        return Hex(x, y, z)

    def hex_add(self, hex_1, hex_2):
        return self.get_hex(
                hex_1.get_x() + hex_2.get_x(),
                hex_1.get_y() + hex_2.get_y(),
                hex_1.get_z() + hex_2.get_z(),
            )

    def hex_subtract(self, hex_1, hex_2):
        return self.get_hypotheical_hex(
                hex_1.get_x() - hex_2.get_x(),
                hex_1.get_y() - hex_2.get_y(),
                hex_1.get_z() - hex_2.get_z(),
            )

    def hex_scale(self, input_hex, scale):
        return self.get_hex(
                input_hex.get_x() * scale,
                input_hex.get_y() * scale,
                input_hex.get_z() * scale,
            )

    def hex_rotate_left(self, input_hex):
        return self.get_hex(
                x=-input_hex.get_z(),
                y=-input_hex.get_x(),
                z=-input_hex.get_y(),
            )

    def hex_rotate_right(self, input_hex):
        return self.get_hex(
                x=-input_hex.get_y(),
                y=-input_hex.get_z(),
                z=-input_hex.get_x(),
            )

    def get_hex_direction(self, direction):
        return self._directions[direction]

    def get_hex_neighbor(self, input_hex, direction):
        return self.hex_add(
                input_hex,
                self.get_hex_direction(direction)
            )

    def get_neighbors(self, input_hex):
        neighbors = []
        for x in range(0, 6):
            neighbors.append(self.get_hex_neighbor(input_hex, x))

        return neighbors

    def get_hex_diagonal_neighbor(self, input_hex, direction):
        return hex_add(
                input_hex,
                self._diagonals[direction]
            )

    def hex_length(self, input_hex):
        hex_sum = (
                abs(input_hex.get_x()) +
                abs(input_hex.get_y()) +
                abs(input_hex.get_z())
            )
        return hex_sum // 2

    def distance(self, hex_1, hex_2):
        return self.hex_length(self.hex_subtract(hex_1, hex_2))

    def hex_round(self, h):
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

    def hex_lerp(self, hex_1, hex_2, t):
        return self.get_hex(
                hex_1.get_x() * (1 - t) + hex_2.get_x() * t,
                hex_1.get_y() * (1 - t) + hex_2.get_y() * t,
                hex_1.get_z() * (1 - t) + hex_2.get_z() * t
            )

    def hex_linedraw(self, hex_1, hex_2):
        distance = hex_distance(hex_1, hex_2)
        
        hex_1_nudge = Hex(
                hex_1.get_x() + 0.000001,
                hex_1.get_y() + 0.000001,
                hex_1.get_z() - 0.000002
            )

        hex_2_nudge = Hex(
                hex_2.get_x() + 0.000001,
                hex_2.get_y() + 0.000001,
                hex_2.get_z() - 0.000002
            )

        results = []
        
        step = 1.0 / max(distance, 1)
        
        for i in range(0, distance + 1):
            results.append(
                    self.hex_round(
                        self.hex_lerp(
                            hex_1_nudge,
                            hex_2_nudge,
                            step * i,
                        )
                    )
                )

        return results

    def hex_ring(self, center_hex, radius):
        results = []

        current_hex = self.hex_add(
                        center_hex, 
                        self.hex_scale(self.get_hex_direction(4), radius)
                    )

        for direction in range(0, 6):
            for length in range(0, radius):
                results.append(current_hex)
                current_hex = self.get_hex_neighbor(current_hex, direction)
        
        return results

    def hex_spiral(self, center_hex, radius):
        results = [center_hex]

        for step in range(0, radius + 1):
            results += self.hex_ring(
                    center_hex=center_hex,
                    radius=step,
                )

        return results

    def get_variance(self, point, radius):
        points = self.hex_spiral(point, radius)
        
        total = 0
        count = 0
        variance = 0

        for tot_point in points:
            total += tot_point.get_a()
            count += 1

        average = total/count

        for var_point in points:
            dif = var_point.get_a() - average
            variance = variance + (dif * dif)

        return variance

    def get_area_average(self, point, radius):
        points = self.hex_spiral(point, radius)
        
        total = 0
        count = 0

        for point in points:
            total += point.get_a()
            count += 1

        average = total/count
        return average
