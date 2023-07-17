from City import City


class Flight:
    def __init__(self, start: City, end: City, flight_connections: list):
        self.__start = start
        self.__end = end
        self.__flight_connections = flight_connections
