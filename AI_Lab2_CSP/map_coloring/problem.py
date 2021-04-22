from csp import CSP
from typing import List, Optional, Dict, Tuple
from helper import tools
from helper.map_generator import BoardDrawer
from helper.exceptions import ProblemNotInitializedException, SolutionNotResolvedException
from random import randint
import math
import copy

from map_coloring.constraints import MapColoringConstraint


class MapColoringProblem:
    def __init__(self, points_number, map_width, map_height):
        self.csp: Optional[CSP] = None
        self.points: List[List[int]] = []
        self.connections: List[List[int]] = []
        self.width = map_width
        self.height = map_height
        self.points_number = points_number
        for i in range(0, points_number):
            self.connections.append([])
        self.colors = {}

    def init_problem(self, colors_number):
        if self.points == []:
            raise ProblemNotInitializedException()
        
        variables: List[Tuple[int, int]] = []
        for p in self.points:
            variables.append((p[0], p[1]))
        domains: Dict[Tuple[int, int], List[int]] = {}
        domain = []
        for i in range(1, colors_number + 1):
            domain.append(i)
        for variable in variables:
            domains[variable] = copy.deepcopy(domain)
        
        self.csp = CSP(variables, domains)
        self.add_constraints()

    
    def add_constraints(self):
        constraints = []
        for p in self.points:
            for p2_idx in self.connections[self.points.index(p)]:
                p2 = self.points[p2_idx]
                if not (p, p2) in constraints and not (p2, p) in constraints:
                    constraints.append((p, p2))
                # self.csp.add_constraint(MapColoringConstraint((p[0], p[1]), (p2[0], p2[1])))
        for c in constraints:
            self.csp.add_constraint(MapColoringConstraint((c[0][0], c[0][1]), (c[1][0], c[1][1])))

    def solve(self):
        if self.csp == None:
            raise ProblemNotInitializedException()
        else:
            solutions = self.csp.backtracking_search(evaluate=self.csp.forward_checking,
                                                     only_first_result=True)
            if solutions == []:
                print("No solution found...")
            else:
                self.print_solutions(solutions)
                self.get_colors_from_solutions(solutions)

    def get_colors_from_solutions(self, solutions):
        i = 0
        for solution in solutions:
            self.colors[i] = []
            for point in self.points:
                self.colors[i].append(solution[(point[0], point[1])])
            i += 1

    def print_solutions(self, solutions):
        for solution in solutions:
            for k in solution:
                color = ""
                if solution[k] == 1:
                    color = "Blue"
                elif solution[k] == 2:
                    color = "Green"
                elif solution[k] == 3:
                    color = "Red"
                elif solution[k] == 4:
                    color = "Yellow"
                elif solution[k] == 5:
                    color == "Light green"
                else:
                    color = solution[k]
                print(f"Point: {k}, color: {color}")
            print()
            print("Visited Nodes:", self.csp.visited_nodes)
                

    def generate_map(self):
        for i in range(self.points_number):
            while True:
                x = randint(1, self.width - 1)
                y = randint(1, self.height - 1)
                if [x, y] not in self.points:
                    self.points.append([x, y])
                    break
        self.generate_connections()


    def print_map(self):
        if self.points == []:
            raise ProblemNotInitializedException()

        if self.colors == []:
            raise SolutionNotResolvedException()

        i = 0
        for k in self.colors.keys():
            colors = self.colors[k]
            print(colors)
            json = {
                "board": self.width,
                "regions": copy.deepcopy(self.points),
                "colors": colors,
                #"colors": [5, 5, 5, 5, 5],
                "connections": self.connections
            }
            #print(json)

            drawer = BoardDrawer(json)
            im = drawer.get_image()
            output_path = f"map_images/generated_map_{i+1}.png"
            im.save(output_path)
            i += 1

    def generate_connections(self):
        done_points = []
        while len(done_points) < len(self.points):
            for p in self.points:
                neighbour = self.find_closest(p)
                if neighbour:
                    self.connections[self.points.index(p)].append(self.points.index(neighbour))
                    self.connections[self.points.index(neighbour)].append(self.points.index(p))
                else:
                    if p not in done_points:
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
                int_pt = tools.find_intersection(point1, point2, p1, p2)
                if int_pt != None and int_pt != point1 and int_pt != point2:
                    return True
                # if tools.intersects(point1, point2, p1, p2):
                #     return True
        return False

    def calculate_distance(self, point, other):
        a = other[0] - point[0]
        b = other[1] - point[1]
        return math.sqrt(a * a + b * b)

