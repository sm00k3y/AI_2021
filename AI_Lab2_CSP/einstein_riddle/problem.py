from typing import Dict, List, Optional
from csp import CSP
from einstein_riddle.constraints import *
from helper.exceptions import ProblemNotInitializedException


class EinsteinRiddleProblem:
    def __init__(self):
        self.colors = ["zolty", "niebieski", "czerwony", "zielony", "bialy"]
        self.nationalities = ["Norweg", "Dunczyk", "Anglik", "Niemiec", "Szwed"]
        self.drinks = ["Woda", "Herbata", "Mleko", "Kawa", "Piwo"]
        self.smokes = ["Cygaro", "Light", "Bez Filtra", "Fajki", "Mentol"]
        self.animals = ["Koty", "Konie", "Ptaki", "Rybki", "Psy"]
        self.houses = [1, 2, 3, 4, 5]
        self.csp = None
    
    def init_problem(self):
        # Houses: 1,2,3,4,5
        variables: List[int] = self.houses
        domains: Dict[int, List[List[str]]] = {}
        for variable in variables:
            domains[variable] = self._generate_domain()
        
        self.csp: CSP[int, str] = CSP(variables, domains)
        self.add_constraints()

    def _generate_domain(self) -> List[List[str]]:
        domain = []
        for c in self.colors:
            for n in self.nationalities:
                for d in self.drinks:
                    for s in self.smokes:
                        for a in self.animals:
                            # IMPORTANT ORDER (c, n, d, s, a)
                            domain.append((c, n, d, s, a))
        return domain

    def add_constraints(self):
        # Wszystkie wartosci musza byc rozne
        self.csp.add_constraint(AllDifferentConstraint(self.houses))
        # 1. W pierwszym domu mieszka Norweg
        self.csp.add_constraint(SingleHouseConstraint(1, 1, self.nationalities[0]))
        # 8. W srodkowym domu pije sie mleko
        self.csp.add_constraint(SingleHouseConstraint(3, 2, self.drinks[2]))

        # Unary constraints
        for house in self.houses:
            # 2. Anglik mieszka w czerwonym domu
            self.csp.add_constraint(
                EveryHouseSingleConstraint(house, 1, self.nationalities[2], 0, self.colors[2]))
            # 4. Dunczyk pija herbate
            self.csp.add_constraint(
                EveryHouseSingleConstraint(house, 1, self.nationalities[1], 2, self.drinks[1]))
            # 6. Mieszkaniec zoltego domu pali cygara
            self.csp.add_constraint(
                EveryHouseSingleConstraint(house, 0, self.colors[0], 3, self.smokes[0]))
            # 7. Niemiec pali fajke
            self.csp.add_constraint(
                EveryHouseSingleConstraint(house, 1, self.nationalities[3], 3, self.smokes[3]))
            # 10. Palacz papierosow bez filtra hoduje ptaki
            self.csp.add_constraint(
                EveryHouseSingleConstraint(house, 3, self.smokes[2], 4, self.animals[2]))
            # 11. Szwed hoduje psy
            self.csp.add_constraint(
                EveryHouseSingleConstraint(house, 1, self.nationalities[4], 4, self.animals[4]))
            # 14. Palacz mentolowych pija piwo
            self.csp.add_constraint(
                EveryHouseSingleConstraint(house, 3, self.smokes[4], 2, self.drinks[4]))
            # 15. W zielonym domu pija sie kawe
            self.csp.add_constraint(
                EveryHouseSingleConstraint(house, 0, self.colors[3], 2, self.drinks[3]))


            # 5. Palacz papierosow light mieszka obok hodowcy kotow
            self.csp.add_constraint(
                NeighbourHouseConstraint(house, 3, self.smokes[1], 4, self.animals[0], self.houses))
            # 9. Palacz papierosow light ma sasiada, ktory pija wode
            self.csp.add_constraint(
                NeighbourHouseConstraint(house, 3, self.smokes[1], 2, self.drinks[0], self.houses))
            # 12. Norweg mieszka obok niebieskiego domu
            self.csp.add_constraint(
                NeighbourHouseConstraint(house, 1, self.nationalities[0], 0, self.colors[1], self.houses))
            # 13. Hodowca koni mieszka obok zoltego domu
            self.csp.add_constraint(
                NeighbourHouseConstraint(house, 4, self.animals[1], 0, self.colors[0], self.houses))

            # self.csp.add_constraint(
            #     LeftHouseConstraint(house, 0, self.colors[3], self.colors[4], self.houses))
            
        # Binary constraints
        for i in range(len(self.houses) - 1):
            house_left = self.houses[i]
            house_right = self.houses[i+1]
            # 3. Zielony dom znajduje sie po lewej stronie domu bialego
            self.csp.add_constraint(
                LeftHouseConstraint(house_left, house_right, self.colors[3], self.colors[4]))

    def solve(self):
        if self.csp == None:
            raise ProblemNotInitializedException()
        else:
            solutions = self.csp.backtracking_search()
            if solutions == []:
                print("No solution found...")
            else:
                self.print_solutions(solutions)

    def print_solutions(self, solutions: List[Dict[int, List[str]]]):
        for solution in solutions:
            for k in sorted(solution.keys()):
                print(f"House {k}: {solution[k]}")
            print()
        print("Visited Nodes:", self.csp.visited_nodes)
        # for k in solution:
        #     print(f"House {k}: {solution[k]}")
