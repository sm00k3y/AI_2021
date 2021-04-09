from einstein_riddle.problem import EinsteinRiddleProblem
from map_coloring.problem import MapColoringProblem


def run_einstein_riddle():
    problem = EinsteinRiddleProblem()
    problem.init_problem()
    problem.solve()

def run_map_coloring():
    problem = MapColoringProblem(5, 16, 16)
    problem.generate_map()
    problem.init_problem(3)
    problem.solve()
    problem.print_map()

if __name__ == "__main__":
    run_map_coloring()
    #run_einstein_riddle()