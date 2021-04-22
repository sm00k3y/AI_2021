from typing import Dict, List
from csp import Constraint

class AllDifferentConstraint(Constraint):
    def __init__(self, houses):
        super().__init__(houses, False)
        
    def satisfied(self, assignment: Dict[int, List[List[str]]]) -> bool:
        for h in assignment:
            house = assignment[h]
            for j in assignment:
                if h != j:
                    house2 = assignment[j]
                    for i in range(len(house)):
                        if house[i] == house2[i]:
                            return False
        return True
                    

# Warunki dotyczace pojdeynczego domu
# 1. Norweg zamieszkuje pierwszy dom
# 8. Mieszkaniec srodkowego domu pija mleko
class SingleHouseConstraint(Constraint):
    def __init__(self, house, pos, value):
        super().__init__([house], True)
        self.h = house
        self.pos = pos
        self.val = value

    def satisfied(self, assignment: Dict[int, List[List[str]]]) -> bool:
        house = assignment[self.h]
        return house[self.pos] == self.val
    

# Pojedynczy waurnek zastosowany do kazdego domu po kolei   
# 2. Anglik mieszka w czerwonym domu
# 4. Dunczyk pija herbate
# 6. Mieszkaniec zoltego domu pali cygara
# 7. Niemiec pali fajke
# 10. Palacz papierosow bez filtra hoduje ptaki
# 11. Szwed hoduje psy
# 14. Palacz mentolowych pija piwo
# 15. W zielonym domu pija sie kawe
class EveryHouseSingleConstraint(Constraint):
    def __init__(self, house, pos1, value1, pos2, value2):
        super().__init__([house], True)
        self.h = house
        self.pos1 = pos1
        self.pos2 = pos2
        self.val1 = value1
        self.val2 = value2

    def satisfied(self, assignment: Dict[int, List[List[str]]]) -> bool:
        house = assignment.get(self.h)
        if house[self.pos1] == self.val1:
            return house[self.pos2] == self.val2
        elif house[self.pos2] == self.val2:
            return house[self.pos1] == self.val1
        else:
            return True


# Warunki dla sasiadujacych domow
# 5. Palacz papierosow light mieszka obok hodowcy kotow
# 9. Palacz papierosow light ma sasiada, ktory pija wode
# 12. Norweg mieszka obok niebieskiego domu
# 13. Hodowca koni mieszka obok zoltego domu
class NeighbourHouseConstraint(Constraint):
    def __init__(self, house, self_pos, self_val, neighbour_pos, neighbour_val, all_houses):
        super().__init__(all_houses, False)
        self.h = house
        self.pos = self_pos
        self.val = self_val
        self.n_pos = neighbour_pos
        self.n_val = neighbour_val
        self.all_houses = all_houses
    
    def satisfied(self, assignment: Dict[int, List[List[str]]]) -> bool:
        house = assignment.get(self.h)

        if not house:
            return True

        left = assignment.get(self.h - 1)
        right = assignment.get(self.h + 1)

        ret1 = True
        ret2 = True
        if self.h - 1 not in self.all_houses:
            ret1 = False
            left = None
        if self.h + 1 not in self.all_houses:
            ret2 = False
            right = None

        if house[self.pos] == self.val:
            if left:
                ret1 = (left[self.n_pos] == self.n_val)
            if right:
                ret2 = (right[self.n_pos] == self.n_val)
            return ret1 or ret2
        elif house[self.n_pos] == self.n_val:
            if left:
                ret1 = (left[self.pos] == self.val)
            if right:
                ret2 = (right[self.pos] == self.val)
            return ret1 or ret2

        return True


# 3. Zielony dom znajduje sie po lewej stronie domu bialego
# class LeftHouseConstraint(Constraint):
#     def __init__(self, house, pos, self_val, right_value, all_houses):
#         super().__init__([house], True)
#         self.house = house
#         self.pos = pos
#         self.val = self_val
#         self.right_val = right_value
#         self.all_houses = all_houses
    
#     def satisfied(self, assignment: Dict[int, List[List[str]]]) -> bool:
#         house = assignment.get(self.house)

#         if house[self.pos] == self.val:
#             if self.house + 1 not in self.all_houses:
#                 return False
#             else:
#                 right = assignment.get(self.house + 1)
#                 if right:
#                     return right[self.pos] == self.right_val
#                 else:
#                     return True
#         elif house[self.pos] == self.right_val:
#             if self.house - 1 not in self.all_houses:
#                 return False
#             else:
#                 left = assignment.get(self.house - 1)
#                 if left:
#                     return left[self.pos] == self.val
#                 else:
#                     return True
#         else:
#             return True

# 3. Zielony dom znajduje sie po lewej stronie domu bialego
class LeftHouseConstraint(Constraint):
    def __init__(self, house_left, house_right, left_val, right_value):
        super().__init__([house_left, house_right], False)
        self.h_left = house_left
        self.h_right = house_right
        self.left_val = left_val
        self.right_val = right_value
    
    def satisfied(self, assignment: Dict[int, List[List[str]]]) -> bool:
        lefty = assignment.get(self.h_left)
        righty = assignment.get(self.h_right)

        if not lefty or not righty:
            return True

        if lefty[0] == self.left_val:
            return righty[0] == self.right_val
        elif righty[0] == self.right_val:
            return lefty[0] == self.left_val
        else:
            return True
