from unittest import TestCase

from City import City
from Colour import Colour
from Connection import Connection
from Deck import Deck
from Flight import Flight
from LongestRouteFinder import findLongestRoute
from Main import _scoreGame, _findPlayerLongestRoute
from Players.TestPlayer import TestPlayer
from Route import Route
from TestUtil import placeConnection


class TestScoring(TestCase):

    def setUp(self):
        self.player_a = TestPlayer(100, 100, Deck(1, 1))
        self.player_b = TestPlayer(100, 100, Deck(1, 1))
        self.place_a = City("a")
        self.place_b = City("b")
        self.place_c = City("c")
        self.place_d = City("d")
        self.place_e = City("e")

        self.connection_a_b = Connection(self.place_a, self.place_b, Colour.ANY, 1, False, 0)
        self.connection_a_c = Connection(self.place_a, self.place_c, Colour.ANY, 2, False, 0)
        self.flight_connection_a_d = Connection(self.place_a, self.place_d, Colour.ANY, 2, False, 0,
                                                True)
        self.connection_b_c = Connection(self.place_b, self.place_c, Colour.ANY, 2, False, 0)
        self.connection_b_d = Connection(self.place_b, self.place_d, Colour.ANY, 4, False, 0)
        self.connection_d_e = Connection(self.place_d, self.place_e, Colour.ANY, 4, False, 0)

        self.connections = [self.connection_a_b, self.connection_a_c, self.flight_connection_a_d,
                            self.connection_b_c, self.connection_b_d,
                            self.connection_d_e]

        self.loc_con_map = {
            self.place_a: [self.connection_a_b, self.connection_a_c, self.flight_connection_a_d],
            self.place_b: [self.connection_a_b, self.connection_b_c,
                           self.connection_b_d],
            self.place_c: [self.connection_a_c, self.connection_b_c],
            self.place_d: [self.connection_d_e, self.connection_b_d, self.flight_connection_a_d],
            self.place_e: [self.connection_d_e]
        }

    def testNoPlayerLocations(self):
        # Checks correct score when no trains placed
        score = _scoreGame([self.player_a], self.connections, {1: 0},
                           self.loc_con_map, [])

        assert score[self.player_a] == 0

    def testScoreOneConnection(self):
        # Tests if the score from one connection_a_b is correct
        self.connection_a_b.use({Colour.YELLOW: 1, Colour.ANY: 0}, Colour.YELLOW, Deck(1,1),
                                self.player_a)

        score = _scoreGame([self.player_a], self.connections, {1: 1}, self.loc_con_map, [])
        assert score[self.player_a] == 1

    def testRouteSingle(self):
        # Check correct score when single route completed
        route = Route(self.place_a, self.place_b, 1)
        self.player_a.addRoute(route)
        placeConnection(self.player_a, self.connection_a_b)
        score = _scoreGame([self.player_a], self.connections, {1: 0}, self.loc_con_map, [])[
            self.player_a]
        correct = score == 11  # 11 as 10 for longest route
        if not correct:
            print(score)
        assert score == 11

    def testLongestRouteSingle(self):
        placeConnection(self.player_a, self.connection_a_b)
        score = _scoreGame([self.player_a], self.connections, {1: 0}, self.loc_con_map, [])[
            self.player_a]
        correct_score = 10
        correct = score == correct_score  # 11 as 10 for longest route
        if not correct:
            print(score)
        assert score == correct_score

    def testLongestRouteTwoOptions(self):
        placeConnection(self.player_a, self.connection_a_b)
        placeConnection(self.player_a, self.connection_a_c)
        longest_route = findLongestRoute(self.place_a, [], self.loc_con_map, self.player_a)[0]
        correct_longest_route = 2
        correct = longest_route == correct_longest_route
        if not correct:
            print(longest_route)
        assert longest_route == 2

    def testLongestRouteCorrectAllocation(self):
        self.player_b.add_to_hand(Colour.YELLOW)
        self.player_b._tryPlace(self.connection_a_b, Colour.YELLOW)
        placeConnection(self.player_a, self.connection_a_c)

        score = _scoreGame([self.player_a, self.player_b], self.connections, {1: 0, 2: 0},
                           self.loc_con_map, [])[self.player_a]
        correct_score = 10
        correct = score == correct_score  # 11 as 10 for longest route
        if not correct:
            print(score)
        assert score == correct_score

    def testLongestCompleteRouteMiddleStart(self):
        placeConnection(self.player_a, self.connection_a_b)
        placeConnection(self.player_a, self.connection_a_c)
        longest_route = _findPlayerLongestRoute(self.loc_con_map, self.player_a)
        correct_longest_route = 3
        correct = longest_route == correct_longest_route
        if not correct:
            print(longest_route)
        assert longest_route == 3

    def testLongestRouteSeparateSections(self):
        placeConnection(self.player_a, self.connection_d_e)
        placeConnection(self.player_a, self.connection_a_b)
        placeConnection(self.player_a, self.connection_a_c)
        longest_route = _findPlayerLongestRoute(self.loc_con_map, self.player_a)
        correct_longest_route = 4
        correct = longest_route == correct_longest_route
        if not correct:
            print(longest_route)
        assert longest_route == 4

    def testLongestRouteStartsOffBranch(self):
        placeConnection(self.player_a, self.connection_a_b)
        placeConnection(self.player_a, self.connection_b_c)
        placeConnection(self.player_a, self.connection_b_d)
        correct_longest = 6
        longest = _findPlayerLongestRoute(self.loc_con_map, self.player_a)
        correct = correct_longest == longest
        if not correct:
            print(longest)
        assert correct_longest == longest

    def testLongestRouteFlightConnection(self):
        placeConnection(self.player_a, self.connection_a_b)
        placeConnection(self.player_a, self.flight_connection_a_d)
        correct_longest = 1
        longest = _findPlayerLongestRoute(self.loc_con_map, self.player_a)
        assert longest == correct_longest

    def testRouteCompletedFlightConnectionNoTerminus(self):
        placeConnection(self.player_a, self.flight_connection_a_d)
        route = Route(self.place_a, self.place_d, 2)
        self.player_a.addRoute(route)
        completed = route.checkCompleted(self.player_a, self.loc_con_map)
        assert not completed

    def testFlightCompleted(self):
        flight = Flight(self.place_a, self.place_d)
        placeConnection(self.player_a, self.flight_connection_a_d)
        completed = flight.checkCompleted(self.player_a, self.loc_con_map)
        assert completed

    def testRouteCompletedViaFlight(self):
        route = Route(self.place_a, self.place_d, 5)
        flight = Flight(self.place_a, self.place_d)
        self.player_a.addRoute(route)
        placeConnection(self.player_a, self.flight_connection_a_d)
        scores = _scoreGame([self.player_a], self.connections, {1: 0, 2: 0, 5: 0}, self.loc_con_map,
                            [flight])
        score = scores[self.player_a]
        assert score == 15, "Score = " + str(score)
