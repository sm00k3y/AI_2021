from csp import Constraint
from typing import List, Dict, Tuple

class MapColoringConstraint(Constraint):
    def __init__(self, point1, point2):
        super().__init__([point1, point2], False)
        self.p1 = point1
        self.p2 = point2

    def satisfied(self, assignment: Dict[Tuple[int, int], int]) -> bool:
        if self.p1 not in assignment or self.p2 not in assignment:
            return True
        return assignment[self.p1] != assignment[self.p2]