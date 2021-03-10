from config import Config
from population import Population

FILE = "zad0.txt"
POPULATION_SIZE = 10

if __name__ == "__main__":
    board_configuration = Config(FILE)
    
    population = Population(board_configuration)
    population.init_population(POPULATION_SIZE)
    population.print_population()