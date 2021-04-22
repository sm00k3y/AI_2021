from einstein_riddle.problem import EinsteinRiddleProblem
from map_coloring.problem import MapColoringProblem
import os
import time

NUMBER_OF_MAP_COLORS = 4
NUMBER_OF_POINTS_ON_MAP = 8
MAP_WIDTH = 32
MAP_HEIGHT = 32


def run_einstein_riddle():
    print("EINSTEIN RIDDLE SOLUTION:")
    problem = EinsteinRiddleProblem()
    problem.init_problem()
    start = time.time()
    problem.solve()
    end = time.time()
    print("Time:", end-start)


def run_map_coloring():
    print("MAP COLORING SOLUTIONS")
    problem = MapColoringProblem(NUMBER_OF_POINTS_ON_MAP, MAP_WIDTH, MAP_HEIGHT)
    problem.generate_map()
    problem.init_problem(NUMBER_OF_MAP_COLORS)
    start = time.time()
    problem.solve()
    end = time.time()
    print("Time:", end-start)
    # problem.print_map()


if __name__ == "__main__":
    run_map_coloring()
    print()
    run_einstein_riddle()
    print()
    # os.system("pause")