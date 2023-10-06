from unittest import TestCase

from City import City
from Colour import Colour
from Connection import Connection
from Deck import Deck
from Exceptions import NotEnoughCardsException, WrongColourException, NotEnoughLocomotivesException, \
    NotEnoughPiecesException, ParallelConnectionException
from Players.TestPlayer import TestPlayer
from Route import Route
from Testing._Util import placeConnection


class Test_Player(TestCase):

    def setUp(self) -> None:
        self.player = TestPlayer(100, 100, Deck(1, 1))

        self.place_a = City("a")
        self.place_b = City("b")
        self.place_c = City("c")

        self.connection_a_b = \
            Connection(self.place_a, self.place_b, Colour.YELLOW, 1, False, 0, False)
        self.connection_a_b_second = \
            Connection(self.place_a, self.place_b, Colour.YELLOW, 1, False, 0, False)
        self.connection_a_b_loco = \
            Connection(self.place_a, self.place_b, Colour.YELLOW, 1, False, 1, False)
        self.long_connection = Connection(self.place_a, self.place_b, Colour.YELLOW, 100, False, 0,
                                          False)

        self.connection_a_b_flight = \
            Connection(self.place_a, self.place_b, Colour.YELLOW, 1, False, 0, True)
        self.long_connection_flight = Connection(self.place_a, self.place_b, Colour.YELLOW, 100,
                                                 False, 0, True)

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
        placeConnection(self.player, self.connection_a_b)
        assert self.player.locations == {self.place_a, self.place_b}

    def testPlaceConnectionNotEnoughCards(self):
        resp = self.player.placeTrain(self.connection_a_b, Colour.YELLOW)
        assert type(resp) == NotEnoughCardsException

    def testPlaceConnectionWrongColour(self):
        resp = self.player.placeTrain(self.connection_a_b, Colour.RED)
        assert type(resp) == WrongColourException

    def testPlaceConnectionNoLocomotives(self):
        resp = self.player.placeTrain(self.connection_a_b_loco, Colour.YELLOW)
        assert type(resp) == NotEnoughLocomotivesException, type(resp)

    def testPlaceConnectionNotEnoughTrains(self):
        placeConnection(self.player, self.long_connection)
        self.player.addToHand(Colour.YELLOW)
        resp = self.player.placeTrain(self.connection_a_b, Colour.YELLOW)
        assert type(resp) == NotEnoughPiecesException, type(resp)
        assert resp.type == "Trains"

    def testPlaceConnectionNotEnoughFlights(self):
        placeConnection(self.player, self.long_connection_flight)
        self.player.addToHand(Colour.YELLOW)
        resp = self.player.placeTrain(self.connection_a_b_flight, Colour.YELLOW)
        assert type(resp) == NotEnoughPiecesException, type(resp)
        assert resp.type == "Flight", resp.type

    def testPlaceConnectionParallelRoute(self):
        placeConnection(self.player, self.connection_a_b)
        self.player.addToHand(Colour.YELLOW)
        resp = self.player.placeTrain(self.connection_a_b_second, Colour.YELLOW)
        assert type(resp) == ParallelConnectionException, type(resp)

