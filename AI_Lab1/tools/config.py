from tools.helper import load_data

class Config:

    def __init__(self, filename):
        self.width, self.height, self.points = load_data(filename)

    def get_board_config(self):
        return self.width, self.height, self.points

    def serialize_points(self):
        pts = []
        for p in self.points:
            pts.append(p[0])
            pts.append(p[1])
        return pts