from unittest import TestCase

from City import City
from Colour import Colour
from Connection import Connection
from Deck import Deck
from Players.TestPlayer import TestPlayer
from Route import Route


class Test_Player(TestCase):

    def setUp(self) -> None:
        self.player = TestPlayer(100, 100, Deck(1, 1))

        self.place_a = City("a")
        self.place_b = City("b")

        self.connection_a_b = Connection(self.place_a, self.place_b, Colour.ANY, 1, False, 0, False)
        self.route_a_b = Route(self.place_a, self.place_b, 1)

    def testAddToHand(self):
        self.player.addToHand(Colour.RED)
        hand = self.player.hand
        assert hand[Colour.RED] == 1

    def testRoutesStartsEmpty(self):
        assert len(self.player.routes) == 0

    def testAddingRoute(self):
        self.player.addRoute(self.route_a_b)
        assert len(self.player.routes) == 1

    def testLocationsStartsEmpty(self):
        assert len(self.player.locations) == 0

    def testLocationAddedWhenTrainPlaced(self):
        self.player.addToHand(Colour.YELLOW)
        self.player.placeTrain(self.connection_a_b, Colour.YELLOW)
        assert self.player.locations == {self.place_a, self.place_b}

