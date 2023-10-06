import warnings

from Colour import Colour
from Connection import Connection
from Deck import Deck
from Players.DumbPlayer import DumbPlayer
from Route import Route


class TestPlayer(DumbPlayer):

    def __init__(self, trains: int, flight_trains: int, deck: Deck):
        super().__init__(trains, flight_trains, deck)
        warnings.warn("This is for testing use only")

    def addRoute(self, route: Route):
        self._routes.append(route)

    def placeTrain(self, connection: Connection, colour: Colour) -> Exception:
        return self._tryPlace(connection, colour)
