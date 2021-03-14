from genetic_algorithm.pcb_board import PCB_board
from tools.config import Config
from tools.exceptions import PopulationNotInitialized, CannotSelectParent, CannotGetChildFromCrossover
from const import ROULETTE_EPSILON, CROSSOVER_PROBABILITY
import random
import copy

class Population:

    def __init__(self, configuration: Config, population_size):
        self.config = configuration
        self.population = []
        self.population_size = population_size

    def init_population(self):
        for _ in range(self.population_size):
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
        if self.population == []:
            raise PopulationNotInitialized()

        for board in self.population:
            board.calculate_fitness()
                
    def select_and_crossover(self):
        for _ in range(self.population_size):
            # Select parents
            parent1, parent2 = self.select_parents_roulette()

            # Crossover (uniform) to produce a child
            new_child = PCB_board(self.config)
            if CROSSOVER_PROBABILITY > random.random():
                new_child.crossover(parent1, parent2)
            else:
                new_child = copy.deepcopy(min(parent1, parent2, key=lambda x: x.fitness))

            if new_child.paths == []:
                raise CannotGetChildFromCrossover()

            # Mutate new child
            new_child.mutate()

            # Add child to population
            self.population.append(new_child)
        
        # Remove previous population, leving only the new population
        del self.population[0:self.population_size]


    def select_parents_roulette(self):
        weight_sum = self.prepare_weights()

        parent1 = self.get_one_parent_roulette(weight_sum)
        parent2 = None

        while parent2 == parent1: # we can find a better way than while loop
            parent2 = self.get_one_parent_roulette(weight_sum)

        if parent1 == None or parent2 == None:
            raise CannotSelectParent()

        return parent1, parent2

    def prepare_weights(self):
        max_fitness = -1
        weight_sum = 0
        for board in self.population:
            if board.fitness > max_fitness:
                max_fitness = board.fitness

        if max_fitness == -1:
            raise CannotSelectParent()

        for board in self.population:
            w = max_fitness - board.fitness + ROULETTE_EPSILON
            board.roulette_weight = w
            weight_sum += w

        return weight_sum

    def get_one_parent_roulette(self, weight_sum):
        rand = random.randint(0, weight_sum)
        running_sum = 0

        for board in self.population:
            running_sum += board.roulette_weight
            if running_sum > rand:
                return board
        
        # Shouldn't get to this place
        return None