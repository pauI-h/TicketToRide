from unittest import TestCase

from City import City
from Colour import Colour
from Connection import Connection
from Deck import Deck
from Main import scoreGame, findLongestRoute
from Players.TestPlayer import TestPlayer
from Route import Route


class TestScoring(TestCase):

    def setUp(self):
        self.player = TestPlayer(0, Deck(1, 1))
        self.place_a = City("a")
        self.place_b = City("b")
        self.place_c = City("c")
        self.connection_a_b = Connection(self.place_a, self.place_b, Colour.ANY, 1, False, 0)
        self.connection_a_c = Connection(self.place_a, self.place_c, Colour.ANY, 2, False, 0)
        self.connections = [self.connection_a_b, self.connection_a_c]
        self.loc_con_map = {self.place_a: [self.connections[0], self.connections[1]],
                            self.place_b: [self.connections[0]],
                            self.place_c: [self.connections[1]]}

    def testNoPlayerLocations(self):
        # Checks correct score when no trains placed
        score = scoreGame([self.player], self.connections, {1: 0},
                          self.loc_con_map)

        assert score[self.player] == 0

    def testScoreOneConnection(self):
        # Tests if the score from one connection_a_b is correct
        self.connection_a_b.use({Colour.YELLOW: 1, Colour.ANY: 0}, Colour.YELLOW, None, self.player)

        score = scoreGame([self.player], self.connections, {1: 1}, self.loc_con_map)
        assert score[self.player] == 1

    def testRouteSingle(self):
        # Check correct score when single route completed
        route = Route(self.place_a, self.place_b, 1)
        self.player.addRoute(route)
        self.player.add_to_hand(Colour.YELLOW)
        self.player._tryPlace(self.connection_a_b, Colour.YELLOW)
        score = scoreGame([self.player], self.connections, {1: 0}, self.loc_con_map)[self.player]
        correct = score == 11  # 11 as 10 for longest route
        if not correct:
            print(score)
        assert score == 11

    def testLongestRouteSingle(self):
        self.player.add_to_hand(Colour.YELLOW)
        self.player._tryPlace(self.connection_a_b, Colour.YELLOW)
        score = scoreGame([self.player], self.connections, {1: 0}, self.loc_con_map)[self.player]
        correct_score = 10
        correct = score == correct_score  # 11 as 10 for longest route
        if not correct:
            print(score)
        assert score == correct_score

    def testLongestRouteTwoOptions(self):
        self.player.add_to_hand(Colour.YELLOW)
        self.player._tryPlace(self.connection_a_b, Colour.YELLOW)
        self.player.add_to_hand(Colour.YELLOW)
        self.player.add_to_hand(Colour.YELLOW)
        self.player._tryPlace(self.connection_a_c, Colour.YELLOW)
        longest_route = findLongestRoute(self.place_a, [], self.loc_con_map, self.player)[0]
        correct_longest_route = 2
        correct = longest_route == correct_longest_route
        if not correct:
            print(longest_route)
        assert longest_route == 2
