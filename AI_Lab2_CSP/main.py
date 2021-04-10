from einstein_riddle.problem import EinsteinRiddleProblem
from map_coloring.problem import MapColoringProblem
import os

NUMBER_OF_MAP_COLORS = 4
NUMBER_OF_POINTS_ON_MAP = 5
MAP_WIDTH = 16
MAP_HEIGHT = 16


def run_einstein_riddle():
    print("EINSTEIN RIDDLE SOLUTION WITH BACKTRACKING:")
    problem = EinsteinRiddleProblem()
    problem.init_problem()
    problem.solve()


def run_map_coloring():
    print("MAP COLORING SOLUTION")
    problem = MapColoringProblem(NUMBER_OF_POINTS_ON_MAP, MAP_WIDTH, MAP_HEIGHT)
    problem.generate_map()
    problem.init_problem(NUMBER_OF_MAP_COLORS)
    problem.solve()
    problem.print_map()


if __name__ == "__main__":
    run_map_coloring()
    print()
    run_einstein_riddle()
    print()
    os.system("pause")