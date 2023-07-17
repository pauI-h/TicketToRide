from City import City
from MultiStepPath import MultiStepPath
from Players.Player import Player


class Flight(MultiStepPath):
    def __init__(self, start: City, end: City):
        super().__init__(start, end)

    def checkCompleted(self, player: Player, city_connection_map: dict):
        return self.checkCompletedGeneral(player, city_connection_map, True)

