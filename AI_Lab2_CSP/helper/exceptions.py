class ProblemNotInitializedException(Exception):
    def __init__(self):
        super().__init__("You must first initialize the problem!")


class SolutionNotResolvedException(Exception):
    def __init__(self):
        super().__init__("Try to first initialize and SOLVE the problem")