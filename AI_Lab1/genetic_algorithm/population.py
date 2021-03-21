from genetic_algorithm.pcb_board import PCB_board
from tools.config import Config
from tools.exceptions import PopulationNotInitialized, CannotSelectParent, CannotGetChildFromCrossover
from const import ROULETTE_EPSILON, CROSSOVER_PROBABILITY
import random
import copy
from PIL import Image
from tools.image_generator import BoardDrawer


class Population:

    def __init__(self, configuration: Config, population_size):
        self.config = configuration
        self.population = []
        self.population_size = population_size

        self.max_fitness = -1
        self.avg_fitness = -1
        self.min_fitness = -1

        self.best_individual = None

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
        best, second = self.get_two_best_individuals()
        self.population.append(best)
        self.population.append(second)

        for _ in range(self.population_size - 2): # -2, becuase two best are already from previous population
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


    def get_two_best_individuals(self):
        first = self.population[0]
        second = self.population[0]
        sum_fit = 0
        for board in self.population:
            sum_fit += board.fitness
            if board.fitness < first.fitness:
                second = first
                first = board
            elif board.fitness < second.fitness:
                second = board
        self.min_fitness = first.fitness
        self.avg_fitness = sum_fit / len(self.population)
        return copy.deepcopy(first), copy.deepcopy(second)


    def select_parents_roulette(self):
        weight_sum = self.prepare_weights()

        parent1 = self.get_one_parent_roulette(weight_sum)
        parent2 = None

        while parent2 == parent1 or parent2 == None: # Always draw different parents
            parent2 = self.get_one_parent_roulette(weight_sum)

        if parent1 == None or parent2 == None:
            raise CannotSelectParent()

        return parent1, parent2

    def prepare_weights(self):
        self.max_fitness = -1
        weight_sum = 0
        for board in self.population:
            if board.fitness > self.max_fitness:
                self.max_fitness = board.fitness

        if self.max_fitness == -1:
            raise CannotSelectParent()

        for board in self.population:
            w = self.max_fitness - board.fitness + ROULETTE_EPSILON
            board.roulette_weight = w
            weight_sum += w

        return weight_sum

    def get_one_parent_roulette(self, weight_sum):
        rand = random.randint(0, weight_sum - 1)
        running_sum = 0

        for board in self.population:
            running_sum += board.roulette_weight
            if running_sum > rand:
                return board
        
        # Shouldn't get to this place
        return None

    def evaluate_population(self):
        return self.min_fitness, self.max_fitness, self.avg_fitness

    def save_best(self, generation):
        json = self.create_json(generation)
        drawer = BoardDrawer(json)
        im = drawer.get_image()
        output_path = "best_individuals/best_from_gen_{gen}.png".format(gen = generation)
        im.save(output_path)

    def create_json(self, generation):
        json = {
            "board": [self.config.width, self.config.height], \
            "generation": generation, \
            "fitness": self.min_fitness, \
            "points": self.config.serialize_points(), \
            "paths": self.get_best().serialize_paths() 
            }
        return json

    def get_best(self):
        best = self.population[0]
        for board in self.population:
            if board.fitness < best.fitness:
                best = board
        self.min_fitness = copy.deepcopy(best.fitness)
        return board
    