from PCB_board import PCB_board
from config import Config

class Population:

    def __init__(self, configuration: Config):
        self.config = configuration
        self.population = []

    def init_population(self, population_size):
        for _ in range(population_size):
            board = PCB_board(self.config)
            board.init_paths()
            self.population.append(board)

    def print_population(self):
        i = 1
        for board in self.population:
            print("========= INDIVIDUAL ", i, " ============\n")
            board.print_paths()
            print("\nFitness: ", board.fitness)
            print("\n")
            i += 1

    def calculate_fitness(self):
        for board in self.population:
            board.calculate_fitness()
