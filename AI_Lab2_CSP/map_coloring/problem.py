from csp import CSP
from typing import List, Optional
from helper import tools
from helper.map_generator import BoardDrawer
from random import randint
import math


class MapColoringProblem:
    def __init__(self):
        self.csp: Optional[CSP] = None
        self.points: List[List[int]] = []
        self.connections: List[List[int]] = []
        self.width = -1
        self.height = -1
        self.points_number = -1

    def init_problem(self, points_number, map_width, map_height):
        self.width = map_width
        self.height = map_height
        self.points_number = points_number
        for i in range(0, points_number):
            self.connections.append([])

    def generate_map(self):
        for i in range(self.points_number):
            while True:
                x = randint(0, self.width)
                y = randint(0, self.height)
                if [x, y] not in self.points:
                    self.points.append([x, y])
                    break
        
        self.generate_connections()

    def print_map(self):
        json = {
            "board": self.width,
            "regions": self.points,
            "colors": [1, 2, 3, 2, 3],
            "connections": self.connections
        }
        print(json)
        drawer = BoardDrawer(json)
        im = drawer.get_image()
        output_path = "map_images/generated_map.png"
        im.save(output_path)

    def generate_connections(self):
        done_points = []
        while len(done_points) < len(self.points):
            for p in self.points:
                neighbour = self.find_closest(p)
                if neighbour:
                    self.connections[self.points.index(p)].append(self.points.index(neighbour))
                    self.connections[self.points.index(neighbour)].append(self.points.index(p))
                else:
                    done_points.append(p)


    def find_closest(self, point) -> List[int]:
        min_distance = self.width * self.height
        closest = None
        pt_index = self.points.index(point)
        for other in self.points:
            if other != point and self.points.index(other) not in self.connections[pt_index]:
                if not self.intersects(point, other):
                    distance = self.calculate_distance(point, other)
                    if distance < min_distance:
                        closest = other
                        min_distance = distance
        return closest


    def intersects(self, point1, point2):
        for p1 in self.points:
            for p2_idx in self.connections[self.points.index(p1)]:
                p2 = self.points[p2_idx]
                if tools.intersects(point1, point2, p1, p2):
                    return True
        return False

    def calculate_distance(self, point, other):
        a = other[0] - point[0]
        b = other[1] - point[1]
        return math.sqrt(a * a + b * b)

