from config import Config
from population import Population
import sys

FILE = "zad0.txt"
POPULATION_SIZE = 10

if __name__ == "__main__":
    if len(sys.argv) > 1:
        FILE = sys.argv[1]
    board_configuration = Config(FILE)
    
    population = Population(board_configuration)

    population.init_population(POPULATION_SIZE)
    population.calculate_fitness()

    population.print_population()