from tools.config import Config
from genetic_algorithm.population import Population
import sys
import os

FILE = "zad0.txt"
POPULATION_SIZE = 10

if __name__ == "__main__":
    if len(sys.argv) > 1:
        FILE = sys.argv[1]
    board_configuration = Config(FILE)

    best_fitness = []
    worst_fitness = []
    avg_fitness = []
    
    population = Population(board_configuration, POPULATION_SIZE)

    population.init_population()
    population.calculate_fitness()

    population.print_population()

    for i in range(50):
        population.select_and_crossover()
        population.calculate_fitness()

        best, worst, avg = population.evaluate_population()

        best_fitness.append(best)
        worst_fitness.append(worst)
        avg_fitness.append(avg)

        # if i % 10 == 0:
        #     population.show_best(i+1)

    population.print_population()

    # os.system("pause")