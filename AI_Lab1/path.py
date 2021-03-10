from const import UP, DOWN, LEFT, RIGHT, HIGHIER_PROBABILITY
import random
import copy

class Path:

    def __init__(self, start_point, end_point, board_width, board_height):
        self.start = start_point
        self.end = end_point
        self.b_width = board_width
        self.b_height = board_height
        self.current_position = copy.deepcopy(start_point)
        self.previous_direction = -24
        self.segments = []


    def randomize(self):
        while self.current_position != self.end:
            rand_vec = self.get_random_vector()

            self.next_position(rand_vec)

            one_line = self.previous_direction + rand_vec[0]
            if one_line == 1 or one_line == 5 or self.previous_direction == rand_vec[0]:
                self.fix_vector(rand_vec, one_line)
            else:
                self.segments.append(rand_vec)
                self.previous_direction = rand_vec[0]


    def get_random_vector(self):
            
        dir_probabilities = self.calculate_direction_probabilities()

        next_dir = self.select_direction(dir_probabilities)

        if next_dir == UP:
            length = random.randint(1, self.b_height - self.current_position[1])
        elif next_dir == DOWN:
            length = random.randint(1, self.current_position[1])
        elif next_dir == LEFT:
            length = random.randint(1, self.current_position[0])
        else:
            length = random.randint(1, self.b_width - self.current_position[0])

        return [next_dir, length]


    def calculate_direction_probabilities(self):

        up = 1
        down = 1
        right = 1
        left = 1

        if self.end[0] - self.current_position[0] > 0:
            right = HIGHIER_PROBABILITY
        elif self.end[0] - self.current_position[0] < 0:
            left = HIGHIER_PROBABILITY
        
        if self.end[1] - self.current_position[1] > 0:
            up = HIGHIER_PROBABILITY
        elif self.end[1] - self.current_position[1] < 0:
            down = HIGHIER_PROBABILITY


        # Segments don't go out of the board
        if self.current_position[0] == 0:
            left = 0
        elif self.b_width - self.current_position[0] < 1:
            right = 0

        if self.current_position[1] == 0:
            down = 0
        elif self.b_height - self.current_position[1] < 1:
            up = 0


        probs = [up, down, right, left]

        return probs

    
    def select_direction(self, probs):
        for i in range(len(probs)):
            probs[i] *= random.randint(1, 100)
        
        return probs.index(max(probs))
        

    def next_position(self, vector):
        if vector[0] == UP:
            self.current_position[1] += vector[1]

        elif vector[0] == DOWN:
            self.current_position[1] -= vector[1]

        elif vector[0] == RIGHT:
            self.current_position[0] += vector[1]

        elif vector[0] == LEFT:
            self.current_position[0] -= vector[1]
    

    def fix_vector(self, new_vector, one_line):
        if self.segments[-1][0] == new_vector[0]:
            self.segments[-1][1] += new_vector[1]
        else:
            self.segments[-1][1] -= new_vector[1]
            if self.segments[-1][1] == 0:
                self.segments = self.segments[:-1]
            elif self.segments[-1][1] < 0:
                self.segments[-1][1] = abs(self.segments[-1][1])
                if one_line == 1:
                    self.segments[-1][0] = 1 - self.segments[-1][0]
                else:
                    self.segments[-1][0] = 5 - self.segments[-1][0]
        
        if self.segments == []:
            self.previous_direction = -24
        else:
            self.previous_direction = self.segments[-1][0]
    

    def print_segments(self):
        print(self.segments)


    def length(self):
        length = 0
        for seg in self.segments:
            length += seg[1]
        return length, len(self.segments)
