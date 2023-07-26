from unittest import TestCase

from City import City
from Colour import Colour
from Connection import Connection
from Deck import Deck
from Flight import Flight
from Players.TestPlayer import TestPlayer
from TestUtil import placeConnection


class TestFlight(TestCase):

    def setUp(self) -> None:
        self.player = TestPlayer(100, 100, Deck(1, 1))

    def testFindLongestCompletedPath(self):
        start = City("start")
        useless = City("useless")
        middle = City("middle")
        end = City("end")
        too_far = City("too far")
        connection_useless = Connection(start, useless, Colour.ANY, 10, False, 0, True)
        connection_start_end = Connection(start, end, Colour.ANY, 1, False, 0, True)
        connection_start_mid = Connection(start, middle, Colour.ANY, 1, False, 0, True)
        connection_mid_end = Connection(middle, end, Colour.ANY, 1, False, 0, True)
        connection_too_far = Connection(end, too_far, Colour.ANY, 4, False, 0, True)

        connection_loc_map = {
            start: [connection_useless, connection_start_end, connection_start_mid],
            useless: [connection_useless],
            middle: [connection_start_mid, connection_mid_end],
            end: [connection_start_end, connection_mid_end, connection_too_far],
            too_far: [connection_too_far]
        }
        flight = Flight(start, end)

        placeConnection(self.player, connection_useless)
        placeConnection(self.player, connection_start_end)
        placeConnection(self.player, connection_start_mid)
        placeConnection(self.player, connection_mid_end)
        placeConnection(self.player, connection_too_far)

        assert flight.checkCompleted(self.player, connection_loc_map)
        length = flight.findLongestCompletedPath(self.player, connection_loc_map)
        assert length == 2, "Length = " + str(length)

    def testFlightCompleted(self):
        place_a = City("a")
        place_b = City("b")
        flight_connection_a_b = Connection(place_a, place_b, Colour.ANY, 2, False, 0, True)

        loc_con_map = {
            place_a: [flight_connection_a_b],
            place_b: [flight_connection_a_b]
        }
        flight = Flight(place_a, place_b)
        placeConnection(self.player, flight_connection_a_b)
        completed = flight.checkCompleted(self.player, loc_con_map)
        assert completed
