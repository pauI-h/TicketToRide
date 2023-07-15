from unittest import TestCase

from City import City
from Colour import Colour
from Connection import Connection
from Deck import Deck
from DumbPlayer import DumbPlayer
from Main import scoreGame


class TestScoring(TestCase):
    def testNoPlayerLocations(self):
        player = DumbPlayer(0, Deck(1, 1))
        place_a = City("a")
        place_b = City("b")
        connections = [Connection(place_a, place_b, Colour.ANY, 1, False, 0)]
        score = scoreGame([player], connections, {1: 0}, {place_a: [connections[0]],
                                                          place_b: [connections[0]]})

        assert score[player] == 0

    def testScoreOneConnection(self):
        player = DumbPlayer(0, Deck(1, 1))
        place_a = City("a")
        place_b = City("b")
        connection = Connection(place_a, place_b, Colour.ANY, 1, False, 0)
        connections = [connection]
        connection.use({Colour.YELLOW: 1, Colour.ANY: 0}, Colour.YELLOW, None, player)

        score = scoreGame([player], connections, {1: 1}, {place_a: [connections[0]],
                                                          place_b: [connections[0]]})
        assert score[player] == 1

