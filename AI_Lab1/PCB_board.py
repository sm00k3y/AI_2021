from config import Config
from path import Path

class PCB_board:

    def __init__(self, config: Config):
        self.width, self.height, self.points = config.get_board_config()
        self.paths = []

    def init_paths(self):
        for points in self.points:
            path = Path(points[0], points[1], self.width, self.height)
            path.randomize()
            self.paths.append(path)
    
    def print_paths(self):
        for path in self.paths:
            path.print_segments()
