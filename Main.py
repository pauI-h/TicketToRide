import math

from Auxilary import *
from Colour import Colour
from Deck import Deck
from DumbPlayer import DumbPlayer


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


def turn(players, connections, stop=math.inf) -> int:
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
            score[connection.getController] += len_score_map[connection.getColourAndLength[1]]

    for player in players:  # Counts points from route
        routes = player.getRoutes()
        for route in routes:
            if route.checkCompleted(connections, player, city_connection_map):
                score[player] += route.getValue()

    # TODO Calc Longest route


def game(players, connections):
    stop = math.inf
    while not finished:
        stop = turn(players, connections)
        if stop != math.inf:
            finished = True

    turn(players, connections, stop)

    scoreGame(players, connections, {})


if __name__ == "__main__":
    main("Europe", "Maps")
