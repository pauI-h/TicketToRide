import math
import sys

from Auxilary import *
from Colour import Colour
from Deck import Deck
from Flight import Flight
from LongestRouteFinder import findLongestRoute
from Players.DumbPlayer import DumbPlayer


def _main(map: str, map_folder: str):
    # LOAD the map
    file_name = map_folder + "\\" + map + ".txt"
    cities, connections, city_connection_map, routes = loadMap(file_name)
    for city in cities:
        print(city, end=", ")
    print()
    for con in connections:
        print(con, end=", ")
    print()
    deck = Deck(12, 14)
    print(deck)
    print(deck.deal())
    print(deck)
    col = deck.showBoard()[0]
    deck.getFromBoard(col)
    deck.discard(col)
    print(deck)
    deck.re_add_discarded()
    print(deck)

    players = [DumbPlayer(20, 6, deck)]
    setupMatch(deck, players, 3)

    am_cons = city_connection_map[cities[0]]
    for con in am_cons:
        print(con, end=", ")
    print()

    print(am_cons[2])
    print(am_cons[2].use({Colour.ANY: 0, Colour.RED: 3}, Colour.RED, deck, players[0]))
    print(am_cons[2].use({Colour.ANY: 0, Colour.RED: 0, Colour.YELLOW: 2}, Colour.YELLOW, deck,
                         players[0]))
    print(am_cons[2].use({Colour.ANY: 0, Colour.YELLOW: 2}, Colour.YELLOW, deck, players[0]))
    print(am_cons[2])

    print(am_cons[0].use({Colour.ANY: 2, Colour.YELLOW: 0}, Colour.YELLOW, deck, players[0]))
    print(am_cons[0])

    for route in routes:
        print(route, end=", ")
    print()


def _turn(players, connections, stop=sys.maxsize) -> int:  # Max size doesn't produce type warnings
    end_player = math.inf
    for i in range(max(len(players), stop)):
        player = players[i]
        player._turn(connections)
        if player.trains < 3:
            end_player = i
    return end_player


def _scoreGame(players, connections, len_score_map: dict, city_connection_map: dict, flights: list):
    score = {}
    for player in players:
        score[player] = 0

    for connection in connections:  # Counts the points from trains
        if connection.getController() is not None:
            score[connection.getController()] += len_score_map[connection.getLength()]

    # Add completed flights
    flight: Flight
    for flight in flights:
        for player in players:
            if flight.checkCompleted(player, city_connection_map):
                length = flight.findLongestCompletedPath(player, city_connection_map)
                new_connection = Connection(flight.start, flight.end, Colour.ANY, length, False, 0)
                new_connection.use({Colour.ANY: length}, Colour.ANY, Deck(1, 1), player)
                city_connection_map[flight.start].append(new_connection)
                city_connection_map[flight.end].append(new_connection)

    for player in players:  # Counts points from route
        routes = player.getRoutes()
        for route in routes:
            if route.checkCompleted(player, city_connection_map):
                score[player] += route.getValue()

    longest_len = 0
    longest_players = []
    for player in players:
        total_length = _findPlayerLongestRoute(city_connection_map, player)
        if total_length > longest_len:
            longest_players = [player]
            longest_len = total_length
        elif total_length == longest_len:  # Multiple players can have longest route
            longest_players.append(player)

    if longest_len > 0:  # No points if no routes have been completed
        for player in longest_players:
            score[player] += 10

    return score


def _findPlayerLongestRoute(city_connection_map, player):
    if len(player.getLocations()) == 0:
        return 0
    locations: set = player.getLocations()
    longest_len = -1
    while len(locations) != 0:  # Used to ensure all nodes have been visited
        start_node = sorted(list(locations))[0]
        # Ensures start node is an element of the graph, sorted removes randomness from set
        length_one, edges_one, nodes_seen_one, end_one = \
            findLongestRoute(start_node, [], city_connection_map, player)
        length_two, edges_two, nodes_seen_two, end_two = \
            findLongestRoute(start_node, edges_one, city_connection_map, player)

        # Checks on the _main path
        length_test, edges_test, nodes_seen_test, end_test = \
            findLongestRoute(end_one, [], city_connection_map, player)
        test_start = end_one
        target_end = end_two
        while end_test != target_end:
            target_end = test_start
            test_start = end_test
            length_test, edges_test, nodes_seen_test, end_test = \
                findLongestRoute(test_start, [], city_connection_map, player)

        if length_test > longest_len:
            longest_len = length_test

        locations = locations.difference(nodes_seen_one)
        locations = locations.difference(nodes_seen_two)
    return longest_len


def game(players, connections):
    stop = math.inf
    finished = False
    while not finished:
        stop = _turn(players, connections)
        if stop != math.inf:
            finished = True

    _turn(players, connections, stop)

    _scoreGame(players, connections, {}, {}, [])


if __name__ == "__main__":
    _main("Europe", "Maps")
