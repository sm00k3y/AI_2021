from tools.config import Config
from tools.helper import prepare_folder_for_imgs, make_chart
from genetic_algorithm.population import Population
import sys
import os
from const import CROSSOVER_PROBABILITY, MUTATION_PROBABILITY, UNIFORM_CROSSOVER_PROBABILITY
import time

FILE = "zad1.txt"
POPULATION_SIZE = 100
GENERATIONS = 100


def run_algorithm():
    global FILE

    if len(sys.argv) > 1:
        FILE = sys.argv[1]

    board_configuration = Config(FILE)

    best_fitness = []
    worst_fitness = []
    avg_fitness = []
    
    population = Population(board_configuration, POPULATION_SIZE)

    start = time.time()
    population.init_population()
    population.calculate_fitness()

    #population.print_population()

    for i in range(GENERATIONS):
        population.select_and_crossover()
        population.calculate_fitness()

        if i % 10 == 0:
            population.save_best(i)

        best, worst, avg = population.evaluate_population()

        print("====== GENERATION {i} =======".format(i=i))
        print("Best fitness: {}".format(best))

        best_fitness.append(best)
        worst_fitness.append(worst)
        avg_fitness.append(avg)

    #population.print_population()
    population.save_best(GENERATIONS)

    stop = time.time()

    print("\nTime: {}".format(stop-start))
    print("Worst: {}".format(worst_fitness[-1]))
    print("Best: {}".format(min(best_fitness)))
    print("Avg: {}".format(avg_fitness[-1]))

    make_chart(best_fitness, worst_fitness, avg_fitness)


def print_params():
    print("\n======== GENETIC ALGORITHM ===========")
    print("PARAMS:")
    print("TEST FILE: {}".format(FILE))
    print("POPULATION_SIZE: {}".format(POPULATION_SIZE))
    print("GENERATIONS: {}".format(GENERATIONS))
    print("CROSSOVER_PROBABILITY: {}".format(CROSSOVER_PROBABILITY))
    print("MUTATION_PROBABILITY: {}".format(MUTATION_PROBABILITY))


if __name__ == "__main__":
    prepare_folder_for_imgs()
    print_params()
    run_algorithm()

    #os.system("pause")