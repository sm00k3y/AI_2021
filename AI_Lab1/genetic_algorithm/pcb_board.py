from tools.config import Config
from genetic_algorithm.path import Path
from const import INTERSECTION_PENALTY, OUT_OF_BOARD_LENGTH_PENALTY, OUT_OF_BOARD_SEGMENTS_PENALTY, \
    SUM_OF_SEGMENTS_PENALTY, UP, DOWN, LEFT, RIGHT, UNIFORM_CROSSOVER_PROBABILITY, MUTATION_PROBABILITY
from shapely.geometry import LineString
import random
import copy

class PCB_board:

    def __init__(self, config: Config):
        self.width, self.height, self.points = config.get_board_config()
        self.paths = []
        self.fitness = -1
        self.roulette_weight = -1

    def init_paths(self):
        for points in self.points:
            path = Path(points[0], points[1], self.width, self.height)
            path.randomize()
            self.paths.append(path)

    def calculate_fitness(self):
        length, sum_of_segments = self.calculate_length()
        intersections = self.count_intersections()
        out_of_board_segments = self.calculate_out_of_board()

        self.fitness = length \
            + (intersections * INTERSECTION_PENALTY) \
            + (sum_of_segments * SUM_OF_SEGMENTS_PENALTY) \
            + (out_of_board_segments * OUT_OF_BOARD_SEGMENTS_PENALTY)

        #return self.fitness

    def calculate_length(self):
        length = 0
        seg = 0
        for path in self.paths:
            size, count = path.length()
            length += size
            seg += count
        
        return length, seg

    def count_intersections(self):
        intersections = 0

        for i in range(0, len(self.paths)):
            start_point = self.paths[i].start

            for seg in self.paths[i].segments:
                end_point = self.calculate_end_point(start_point, seg)

                for j in range(i+1, len(self.paths)):
                    start_point2 = self.paths[j].start

                    for seg2 in self.paths[j].segments:
                        end_point2 = self.calculate_end_point(start_point2, seg2)

                        if self.intersects(start_point, end_point, start_point2, end_point2):
                            intersections += 1
                        
                        start_point2 = end_point2

                start_point = end_point

        return intersections

    def calculate_end_point(self, start_point, segment):

        if segment[0] == UP:
            end_point = start_point[0], start_point[1] + segment[1]
        elif segment[0] == DOWN:
            end_point = start_point[0], start_point[1] - segment[1]
        elif segment[0] == LEFT:
            end_point = start_point[0] - segment[1], start_point[1]
        else:
            end_point = start_point[0] + segment[1], start_point[1]

        return end_point

    def intersects(self, start1, end1, start2, end2):
        line1 = LineString([start1, end1])
        line2 = LineString([start2, end2])

        return line1.intersects(line2)


    def calculate_out_of_board(self):
        out_of_board_segments = 0

        for path in self.paths:
            start_point = path.start

            for seg in path.segments:
                end_point = self.calculate_end_point(start_point, seg)

                if self.over_the_board(end_point):
                    out_of_board_segments += 1
                
                start_point = end_point

        return out_of_board_segments
    
    def over_the_board(self, end):
        return end[0] < 0 or end[0] > self.width \
            or end[1] < 0 or end[1] > self.height


    def crossover(self, parent1, parent2):
        for i in range(len(parent1.paths)):
            if UNIFORM_CROSSOVER_PROBABILITY > random.random():
                self.paths[i] = copy.deepcopy(parent1.paths[i])
            else:
                self.paths[i] = copy.deepcopy(parent2.paths[i])

    
    def mutate(self):
        # Mutate every segment in every path with probability: MUTATION_PROBABILITY
        for path in self.paths:
            for i in range(len(path.segments)):
                if MUTATION_PROBABILITY > random.random():
                    path.mutate(i)


    def print_paths(self):
        for path in self.paths:
            print("Start Point: ", path.start, ", End Point: ", path.end)
            path.print_segments()
