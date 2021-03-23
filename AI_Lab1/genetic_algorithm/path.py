from const import UP, DOWN, LEFT, RIGHT, HIGHIER_PROBABILITY, PATH_MOVEMENT_SIZE
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

        # Direction pointing to the end_point will have highier probability
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
    

    def print_segments(self):
        print("Path: ", end="")
        for seg in self.segments:
            if seg[0] == UP:
                print("(UP, ", seg[1], "), ", end="", sep="")
            elif seg[0] == DOWN:
                print("(DOWN, ", seg[1], "), ", end="", sep="")
            elif seg[0] == LEFT:
                print("(LEFT, ", seg[1], "), ", end="", sep="")
            else:
                print("(RIGHT, ", seg[1], "), ", end="", sep="")
        print()


    def length(self):
        length = 0
        for seg in self.segments:
            length += seg[1]
        return length, len(self.segments)


    def mutate(self, index):
        self.a_mutation(index)

    def a_mutation(self, index):
        seg = self.segments[index]
        path_movement = -1 * PATH_MOVEMENT_SIZE if 0.5 > random.random() else PATH_MOVEMENT_SIZE
        segments_to_mutate = []

        # If we need to add one segment to the beggining
        if index == 0:
            if seg[0] == UP or seg[0] == DOWN:
                if path_movement > 0:
                    self.segments.insert(0, [RIGHT, path_movement])
                else:
                    self.segments.insert(0, [LEFT, -1 * path_movement])
            else:
                if path_movement > 0:
                    self.segments.insert(0, [UP, path_movement])
                else:
                    self.segments.insert(0, [DOWN, -1 * path_movement])
            index += 1
        else:
            segments_to_mutate.append(self.segments[index - 1])
        
        # If we need to add one segment to the end
        if index == len(self.segments) - 1:
            if seg[0] == UP or seg[0] == DOWN:
                if path_movement > 0:
                    self.segments.append([LEFT, path_movement])
                else:
                    self.segments.append([RIGHT, -1 * path_movement])
            else:
                if path_movement > 0:
                    self.segments.append([DOWN, path_movement])
                else:
                    self.segments.append([UP, -1 * path_movement])
        else:
            segments_to_mutate.append(self.segments[index + 1])
            if len(segments_to_mutate) == 1:
                path_movement *= -1

        # Any other case of mutation
        for s in segments_to_mutate:
            if ((seg[0] == UP or seg[0] == DOWN) and s[0] == RIGHT) \
                or ((seg[0] == LEFT or seg[0] == RIGHT) and s[0] == UP):
                s[1] += path_movement
            else:
                s[1] -= path_movement
            path_movement *= -1


    def fix_segments(self):
        '''
        Checks if a new vector is in the same or opposite direction of the old one
        If so, it will modify the previous vector instead of just inserting the new one

        Egxample: Previous vector: (RIGHT, 5), New Vector: (LEFT, 3)
        After the method: Vector (RIGHT, 2)

        Example: Previous vector: (RIGHT, 3), New Vector: (LEFT, 5)
        After the method: Vector(LEFT, 2)
        '''
        i = 1
        while i < len(self.segments):
            curr = self.segments[i]
            prev = self.segments[i-1]
            one_line = prev[0] + curr[0]
            if prev[1] == 0:
                del self.segments[i-1]
                i -= 1
            elif prev[1] < 0:
                prev[1] = abs(prev[1])
                if prev[0] == 0 or prev[0] == 1:
                    prev[0] = 1 - prev[0]
                else:
                    prev[0] = 5 - prev[0]
                i -= 1
            elif curr[1] == 0:
                del self.segments[i]
            elif curr[1] < 0:
                curr[1] = abs(curr[1])
                if curr[0] == 0 or curr[0] == 1:
                    curr[0] = 1 - curr[0]
                else:
                    curr[0] = 5 - curr[0]
            elif one_line == 1 or one_line == 5 or curr[0] == prev[0]:
                if prev[0] == curr[0]:
                    prev[1] += curr[1]
                    del self.segments[i]
                    # NOT incrementing i here
                else:
                    prev[1] -= curr[1]
                    del self.segments[i]
                    if prev[1] == 0:
                        del self.segments[i-1]
                    elif prev[1] < 0:
                        prev[1] = abs(prev[1])
                        if one_line == 1:
                            prev[0] = 1 - prev[0]
                        else:
                            prev[0] = 5 - prev[0]
                    i -= 1
            else:
                i += 1

            # Finally (still in while loop)
            if i == 0:
                i += 1

    
    def serialize_singe_path(self):
        path = []

        self.current_position = copy.deepcopy(self.start)
        path.append(copy.deepcopy(self.current_position))

        for seg in self.segments:
            self.next_position(seg)
            path.append(copy.deepcopy(self.current_position))
        
        return path
