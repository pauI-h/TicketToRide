class NotEnoughCardsException(Exception):

    def __init__(self, message):
        pass


class WrongColourException(Exception):
    def __init__(self, message):
        pass


class NotEnoughLocomotivesException(Exception):
    def __init__(self, message):
        pass


class NotEnoughPiecesException(Exception):
    def __init__(self, type):
        self.type = type
        pass


class ParallelConnectionException(Exception):
    def __init__(self, message):
        pass
