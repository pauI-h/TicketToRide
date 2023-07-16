import math
import sys

from Auxilary import *
from Colour import Colour
from Deck import Deck
from Players.DumbPlayer import DumbPlayer
from Players.Player import Player


def main(map: str, map_folder: str):
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
            if route.checkCompleted(connections, player, city_connection_map):
                score[player] += route.getValue()

    longest_len = 0
    longest_players = []
    for player in players:
        if len(player.getLocations()) == 0:
            continue
        start_node = list(player.getLocations())[0]  # Ensures start node is an element of the graph
        length_one, edges = findLongestRoute(start_node, [], city_connection_map, player)
        length_two, edges_two = findLongestRoute(start_node, edges, city_connection_map, player)
        total_length = length_one + length_two
        if total_length > longest_len:
            longest_players = [player]
            longest_len = total_length
        elif total_length == longest_len:
            longest_players.append(player)

    for player in longest_players:
        score[player] += 10

    return score


def findLongestRoute(node: City, seen_edges: list, city_connection_map: dict,
                     player: Player) -> (int, list):
    outward_connections = city_connection_map[node]
    valid_outward = []
    for connection in outward_connections:
        if connection not in seen_edges and connection.getController() == player:
            valid_outward.append(connection)

    if len(valid_outward) == 0:  # No valid continuation from this point
        return 0, []

    elif len(valid_outward) == 1:  # Only one option
        edges_used = seen_edges + valid_outward
        ends = list(valid_outward[0].getLocations())
        ends.remove(node)
        return findLongestRoute(ends[0], edges_used, city_connection_map, player)

    else:  # Go through all the options
        longest = -1
        longest_edges_used = []
        for connection in valid_outward:
            ends = list(connection.getLocations())
            ends.remove(node)
            edges_used = seen_edges + [connection]
            length, new_edges_used = findLongestRoute(ends[0], edges_used, city_connection_map,
                                                      player)
            length += connection.getLength()
            edges_used += new_edges_used
            if length > longest:
                longest_edges_used = edges_used
                longest = length
            if length == longest and len(longest_edges_used) < len(edges_used):
                longest_edges_used = edges_used
                longest = length

        return longest, longest_edges_used


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
