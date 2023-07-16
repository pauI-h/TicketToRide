class City:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __lt__(self, other):
        if type(other) != City:
            raise TypeError("Can only compare cities")
        else:
            return self.name < other.name
