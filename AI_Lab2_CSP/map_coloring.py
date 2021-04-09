from csp import Constraint, CSP
from typing import Dict, List, Optional
from random import randint


class MapColoringConstraint(Constraint):
    def __init__(self, place1: List[int], place2: List[int]):
        super().__init__([place1, place2])
        self.place1: List[int] = place1
        self.place2: List[int] = place2

    def satisfied(self, assignment: Dict[List[int], str]) -> bool:
        # If either place is not in the assignment then it is not
        # yet possible for their colors to be conflicting
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # check the color assigned to place1 is not the same as the
        # color assigned to place2
        return assignment[self.place1] != assignment[self.place2]


class Connection:
    def __init__(self, point1, point2):
        self.node1 = point1
        self.node2 = point2


class MapColoringProblem:
    def __init__(self):
        self.generated = False

    def generate_problem(self, nodes, width, height):
        points = []  # List of Tuples [(x, y)]
        for i in range(0, nodes):
            while True:
                x = randint(0, width)
                y = randint(0, height)
                if (x, y) not in points:
                    points.append((x, y))


