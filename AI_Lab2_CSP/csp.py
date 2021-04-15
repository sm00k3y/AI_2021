from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod
from copy import deepcopy
from helper.default_functions import no_eval, default_val, default_var

V = TypeVar('V') # variable type
D = TypeVar('D') # domain type


# Base class for all constraints
class Constraint(Generic[V, D], ABC):
    # The variables that the constraint is between
    def __init__(self, variables: List[V]):
        self.variables = variables

    # Must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...


# A constraint satisfaction problem consists of variables of type V
# that have ranges of values known as domains of type D and constraints
# that determine whether a particular variable's domain selection is valid
class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]):
        self.variables: List[V] = variables # variables to be constrained
        self.domains: Dict[V, List[D]] = domains # domain of each variable
        self.pruned = {}
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            self.pruned[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[V, D]):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    # Check if the value assignment is consistent by checking all constraints
    # for the given variable against it
    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}, evaluate=no_eval, 
                            choose_var=default_var, sort_val=default_val) -> Optional[Dict[V, D]]:
        # assignment is complete if every variable is assigned (our base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        # Choosing variable with heuristic or first by default
        first: V = choose_var(unassigned)

        # Sorting values with heuristic or NOT sorting by default
        sort_val(first, assignment)

        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                if evaluate(first, local_assignment):
                    result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                    # if we didn't find the result, we will end up backtracking
                    if result is not None:
                        return result
        return None

    def forward_checking(self, variable, assignment) -> bool:
        temp_assignment = assignment.copy()

        for (v, val) in self.pruned[variable]:
            self.domains[v].append(val)
        self.pruned[variable] = []

        for constraint in self.constraints[variable]:
            for cv in constraint.variables:
                if cv != variable and cv not in assignment:
                    for con_val in self.domains[cv]:
                        temp_assignment[cv] = con_val
                        if not constraint.satisfied(temp_assignment):
                            del self.domains[cv][self.domains[cv].index(con_val)]
                            self.pruned[variable].append((cv, con_val))
                        del temp_assignment[cv]
                    if self.domains[cv] == []:
                        return False

        return True

    # MAC - Maintaining Arc Consistency
    def mac(self, current_variable, assignment):
        queue = []
        for constraint in self.constraints[current_variable]:
            for v in constraint.variables:
                if v != current_variable:
                    queue.append((v, current_variable))
        return self.AC3(queue, assignment)

    def AC3(self, queue, assignment={}):
        if queue is None:
            queue = self.prep_queue()

        while len(queue) != 0:
            Xi, Xj = queue.pop(0)
            if self.arc_reduce(Xi, Xj, assignment):
                if self.domains[Xi] == []:
                    return False
                else:
                    for constraint in self.constraints[Xi]:
                        for v in constraint.variables:
                            if v != Xj and (v, Xi) not in queue:
                                queue.append((v, Xi))
        return True

    def prep_queue(self):
        queue = []
        for Xi in self.variables:
            for constraint in self.constraints[Xi]:
                for v in constraint.variables:
                    if v != Xi:
                        queue.append((Xi, v))
        return queue

    def arc_reduce(self, x, y, assignement={}):
        change = False
        temp_assignment = assignement.copy()
        for constraint in self.constraints[x]:
            for vx in self.domains[x]:
                temp_assignment[x] = vx
                if not self.find_value(constraint, y, temp_assignment):
                    del self.domains[x][self.domains[x].index(vx)]
                    change = True
        return change
                    
    def find_value(self, constraint, y, temp_assignment):
        for vy in constraint.variables:
            temp_assignment[y] = vy
            if constraint.satisfied(temp_assignment):
                return True
        del temp_assignment[y]
        return False

    # MRV - Minimum Remaining Values heuristic - for choosing the variable
    def mrv(self, unassigned):
        lowest_num = len(self.domains[unassigned[0]])
        best = unassigned[0]
        for variable in unassigned:
            if len(self.domains[variable]) < lowest_num:
                best = variable
                lowest_num = len(self.domains[variable])
        return best

    # LCV - Least Constraining Value heuristic - for choosing order of values to pick
    def lcv(self, current_variable, assignment):
        conflicts = {}
        local_assignment = assignment.copy()
        for value in self.domains[current_variable]:
            local_assignment[current_variable] = value
            conflicts[value] = self.count_conflicts(value, current_variable, local_assignment)
        
        self.domains[current_variable] = sorted(conflicts, key=conflicts.get)

    def count_conflicts(self, value, variable, assignement):
        count = 0
        for constraint in self.constraints[variable]:
            for v in constraint.variables:
                if v != variable:
                    for other_value in self.domains[v]:
                        assignement[v] = other_value
                        if not constraint.satisfied(assignement):
                            count += 1
                    del assignement[v]
        return count

