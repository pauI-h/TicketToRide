
from Players.DumbPlayer import DumbPlayer
from Route import Route


class TestPlayer(DumbPlayer):

    def addRoute(self, route: Route):
        self._routes.append(route)

    def placeTrain(self, connection, colour):
        self._tryPlace(connection, colour)
