from City import City
from MultiStepPath import MultiStepPath
from Players.Player import Player


class Route(MultiStepPath):
    def __init__(self, start: City, end: City, value: int):
        super().__init__(start, end)
        self.__value = value

    def getInfo(self):
        return self.start, self.end, self.__value

    def getValue(self):
        return self.__value

    def checkCompleted(self, player: Player, city_connection_map: dict):
        return self.checkCompletedGeneral(player, city_connection_map, False)

    def __str__(self):
        return str(super) + " Value: " + str(self.__value)
