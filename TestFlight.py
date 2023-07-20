from unittest import TestCase

from City import City
from Colour import Colour
from Connection import Connection
from Deck import Deck
from Flight import Flight
from Players.TestPlayer import TestPlayer
from TestUtil import placeConnection


class TestFlight(TestCase):
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
        player = TestPlayer(100, 100, Deck(1, 1))
        flight = Flight(start, end)

        placeConnection(player, connection_useless)
        placeConnection(player, connection_start_end)
        placeConnection(player, connection_start_mid)
        placeConnection(player, connection_mid_end)
        placeConnection(player, connection_too_far)

        assert flight.checkCompleted(player, connection_loc_map)
        length = flight.findLongestCompletedPath(player, connection_loc_map)
        assert length == 2, "Length = " + str(length)
