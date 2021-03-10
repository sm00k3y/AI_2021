import helper

class Config:

    def __init__(self, filename):
        self.width, self.height, self.points = helper.load_data(filename)

    def get_board_config(self):
        return self.width, self.height, self.points