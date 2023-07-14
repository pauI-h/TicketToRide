from City import City
from Player import Player


class Route:
    def __init__(self, start: City, end: City, value: int):
        self.__start = start
        self.__end = end
        self.__value = value

    def getInfo(self):
        return self.__start, self.__end, self.__value

    def getValue(self):
        return self.__value

    def checkCompleted(self, connections: list, player: Player, city_connection_map: dict):
        # TODO Add check for if in player locations
        start_found = False
        end_found = False

        nodes = [self.__start]
        nodes_queue = [self.__start]

        start_connections = city_connection_map[self.__start]
        for connection in start_connections:
            if connection.getController() == player:
                start_found = True
                connections.append(connection)

        if not start_found:
            return False

        end_connections = city_connection_map[self.__end]
        for connection in end_connections:
            if connection.getController() == player:
                end_found = True
                break

        if not end_found:
            return False

        while len(nodes_queue) != 0:  # Implements BFS
            node = nodes_queue.pop()
            connection_list = city_connection_map[node]
            for connection in connection_list:
                if connection.getController() == player:
                    locations = connection.getLocations()
                    for location in locations:
                        if location != node:
                            if location == self.__end:
                                return True
                            nodes.append(location)
                            nodes_queue.append(location)
        return False

    def __str__(self):
        return str(self.__start) + "->" + str(self.__end) + " Value: " + str(self.__value)
