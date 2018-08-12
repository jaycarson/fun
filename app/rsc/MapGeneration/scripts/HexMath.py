#!/usr/bin/python

import math


class Hex(object):
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
        self._r = 0
        self._g = 0
        self._b = 0
        self._a = 0
        self._farm_type = ''
        self._house_type = ''

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def get_r(self):
        return self._r

    def get_g(self):
        return self._g

    def get_b(self):
        return self._b

    def get_a(self):
        return self._a

    def get_farm_type(self):
        return self._farm_type

    def get_house_type(self):
        return self._house_type

    def set_r(self, r):
        self._r = r

    def set_g(self, g):
        self._g = g

    def set_b(self, b):
        self._b = b

    def set_a(self, a):
        self._a = a

    def set_farm_type(self, farm_type):
        self._farm_type = farm_type

    def set_house_type(self, house_type):
        self._house_type = house_type

    def set_color(self, r=0, g=0, b=0, a=0):
        self._r = r
        self._g = g
        self._b = b
        self._a = a


class HexMath(object):
    def __init__(self):
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

    def get_hex(self, x, y):
        self.get_hex(x, y, -x-y)

    def get_hex(self, x, y, z):
        return Hex(x, y, z)

    def hex_add(self, hex_1, hex_2):
        return self.get_hex(
                hex_1.get_x() + hex_2.get_x(),
                hex_1.get_y() + hex_2.get_y(),
                hex_1.get_z() + hex_2.get_z(),
            )

    def hex_subtract(self, hex_1, hex_2):
        return self.get_hex(
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
        return self._hex_directions[direction]

    def get_hex_neighbor(self, input_hex, direction):
        return self.hex_add(
                input_hex,
                self.get_hex_direction(direction)
            )

    def get_neighbors(self, input_hex):
        neighbors = []
        for x in range(0, 6):
            neighbors.append(self.get_neighbor(input_hex, x))

        return neighbors

    def get_hex_diagonal_neighbor(self, input_hex, direction):
        return hex_add(
                input_hex,
                self._diagonals[direction]
            )

    def get_hex_length(self, input_hex):
        hex_sum = (
                abs(input_hex.get_x()) +
                abs(input_hex.get_y()) +
                abs(input_hex.get_z())
            )
        return hex_sum // 2

    def get_hex_distance(self, hex_1, hex_2):
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

    def hex_ring(self, x, y, radius):
        results = []
        center_hex = self.get_hex(x, y)

        current_hex = hex_add(
                        center_hex, 
                        hex_scale(hex_direction(4), radius)
                    )

        for direction in range(0, 6):
            for length in range(0, radius):
                results.append(current_hex)
                current_hex = self.cube_neighbor(current_hex, direction)
        
        return results

    def hex_spiral(self, x, y, radius):
        center_hex = self.get_hex(x, y)
        results = [center_hex]
        
        for step in range(1, radius):
            results += hex_ring(
                    x=x,
                    y=y,
                    radius=step,
                )
        
        return results

    '''
    Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
    Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
    layout_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
    layout_flat = Orientation(3.0 / 2.0, 0.0, math.sqrt(3.0) / 2.0, math.sqrt(3.0), 2.0 / 3.0, 0.0, -1.0 / 3.0, math.sqrt(3.0) / 3.0, 0.0)
    
    def hex_to_pixel(layout, h):
        M = layout.orientation
        size = layout.size
        origin = layout.origin
        x = (M.f0 * h.q + M.f1 * h.r) * size.x
        y = (M.f2 * h.q + M.f3 * h.r) * size.y
        return Point(x + origin.x, y + origin.y)
    
    def pixel_to_hex(layout, p):
        M = layout.orientation
        size = layout.size
        origin = layout.origin
        pt = Point((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
        q = M.b0 * pt.x + M.b1 * pt.y
        r = M.b2 * pt.x + M.b3 * pt.y
        return Hex(q, r, -q - r)
    
    def hex_corner_offset(layout, corner):
        M = layout.orientation
        size = layout.size
        angle = 2.0 * math.pi * (M.start_angle - corner) / 6
        return Point(size.x * math.cos(angle), size.y * math.sin(angle))
    
    def polygon_corners(layout, h):
        corners = []
        center = hex_to_pixel(layout, h)
        for i in range(0, 6):
        offset = hex_corner_offset(layout, i)
        corners.append(Point(center.x + offset.x, center.y + offset.y))
        return corners
    '''
