
class WrongBoardSizeFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class WrongStartEndPointsFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class PopulationNotInitialized(Exception):
    def __init__(self):
        super().__init__("Population not initialized!")


class CannotSelectParent(Exception):
    def __init__(self):
        super().__init__("Fitness not calculated or population not initialized!")


class CannotGetChildFromCrossover(Exception):
    def __init__(self):
        super().__init__("Crossover failed or was not initiated!")
