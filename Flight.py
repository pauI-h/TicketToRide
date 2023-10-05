from City import City
from LongestRouteFinder import findLongestRoute
from MultiStepPath import MultiStepPath
from Players.Player import Player


class Flight(MultiStepPath):
    def __init__(self, start: City, end: City):
        super().__init__(start, end)

    def checkCompleted(self, player: Player, city_connection_map: dict):
        # TODO check they have a non-flight connection into the end cities
        return self.checkCompletedGeneral(player, city_connection_map, True)

    def findLongestCompletedPath(self, player: Player, city_connection_map: dict):
        """
        Gets the longest path between the player used to complete the path
        :param player:
        :param city_connection_map:
        :return:
        """

        return findLongestRoute(self.start, [], city_connection_map, player, self.end, True)[0]

