
class WrongBoardSizeFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class WrongStartEndPointsFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class PopulationNotInitialized(Exception):
    def __init__(self):
        super.__init__("Population not initialized!")
