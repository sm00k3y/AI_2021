from tools.config import Config
from genetic_algorithm.population import Population
import sys
import os

FILE = "zad1.txt"
POPULATION_SIZE = 10

if __name__ == "__main__":
    if len(sys.argv) > 1:
        FILE = sys.argv[1]
    board_configuration = Config(FILE)
    
    population = Population(board_configuration)

    population.init_population(POPULATION_SIZE)
    population.calculate_fitness()

    population.print_population()

    for _ in range(10):
        population.select_and_crossover()
        population.mutate()
        population.calculate_fitness()

    # os.system("pause")