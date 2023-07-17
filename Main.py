import math
import sys

from Auxilary import *
from Colour import Colour
from Deck import Deck
from Players.DumbPlayer import DumbPlayer
from Players.Player import Player


def main(map: str, map_folder: str):
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

    players = [DumbPlayer(20, deck)]
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


def turn(players, connections, stop=sys.maxsize) -> int:  # Max size doesn't produce type warnings
    end_player = math.inf
    for i in range(max(len(players), stop)):
        player = players[i]
        player.turn(connections)
        if player.trains < 3:
            end_player = i
    return end_player


def scoreGame(players, connections, len_score_map: dict, city_connection_map: dict):
    score = {}
    for player in players:
        score[player] = 0

    for connection in connections:  # Counts the points from trains
        if connection.getController() is not None:
            score[connection.getController()] += len_score_map[connection.getLength()]

    for player in players:  # Counts points from route
        routes = player.getRoutes()
        for route in routes:
            if route.checkCompleted(player, city_connection_map):
                score[player] += route.getValue()

    longest_len = 0
    longest_players = []
    for player in players:
        total_length = findPlayerLongestRoute(city_connection_map, player)
        if total_length > longest_len:
            longest_players = [player]
            longest_len = total_length
        elif total_length == longest_len:  # Multiple players can have longest route
            longest_players.append(player)

    if longest_len > 0:  # No points if no routes have been completed
        for player in longest_players:
            score[player] += 10

    return score


def findPlayerLongestRoute(city_connection_map, player):
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

        # Checks on the main path
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


def findLongestRoute(node: City, seen_edges: list, city_connection_map: dict,
                     player: Player) -> (int, list, set, City):
    outward_connections = city_connection_map[node]
    valid_outward = []
    for connection in outward_connections:  # Gets just the usable routes
        if not connection.flight_connection and connection not in seen_edges and connection.getController() == player:
            valid_outward.append(connection)

    nodes_seen = {node}  # The current node is always seen
    if len(valid_outward) == 0:  # No valid continuation from this point
        return 0, [], nodes_seen, node

    elif len(valid_outward) == 1:  # Only one option
        edges_used = seen_edges + valid_outward
        ends = list(valid_outward[0].getLocations())
        ends.remove(node)
        next_len, next_edges, new_nodes, end = findLongestRoute(ends[0], edges_used,
                                                                city_connection_map, player)
        nodes_seen = nodes_seen.union(new_nodes)
        return next_len + valid_outward[0].getLength(), next_edges + edges_used, nodes_seen, end

    else:  # Go through all the options
        longest = -1
        longest_edges_used = []
        furthest_end = None
        for connection in valid_outward:
            ends = list(connection.getLocations())
            ends.remove(node)
            nodes_seen.add(ends[0])  # Adds the node being checked to the list of nodes seen
            edges_used = seen_edges + [connection]  # Tracks the edges used so far

            length, new_edges_used, new_nodes_seen, end = \
                findLongestRoute(ends[0], edges_used, city_connection_map, player)

            length += connection.getLength()
            # Adds the length of the current connection to the follow on connections
            edges_used += new_edges_used
            nodes_seen = nodes_seen.union(new_nodes_seen)
            if length > longest:
                # Updates with the longest route found
                longest_edges_used = edges_used
                longest = length
                furthest_end = end
            if length == longest and len(longest_edges_used) < len(edges_used):
                # Uses the longest path with the lowest number of edges
                longest_edges_used = edges_used
                longest = length
                furthest_end = end

        return longest, longest_edges_used, nodes_seen, furthest_end


def game(players, connections):
    stop = math.inf
    finished = False
    while not finished:
        stop = turn(players, connections)
        if stop != math.inf:
            finished = True

    turn(players, connections, stop)

    scoreGame(players, connections, {}, {})


if __name__ == "__main__":
    main("Europe", "Maps")
