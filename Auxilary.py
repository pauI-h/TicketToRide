from City import City
from Colour import Colour
from Connection import Connection
from Deck import Deck
from Route import Route


def loadMap(file_name: str):
    cities = []
    connections = []
    routes = []
    city_connection_map = {}
    file = open(file_name, "r")
    lines = file.readlines()
    file.close()

    current = cities
    title_list_map = {"Connections": connections, "Routes": routes}
    ab_city_map = {}

    for line in lines:
        line = line.strip("\n")

        if line[:4] == "####":
            title = line[5:]
            current = title_list_map[title]
            continue

        if current == cities:
            split_line = line.split(", ")
            city = City(split_line[0])
            ab_city_map[split_line[1]] = city
            current.append(city)
            city_connection_map[city] = []

        if current == connections:
            split_line = line.split(" ")
            start = ab_city_map[split_line[0]]
            end = ab_city_map[split_line[1]]
            colour = Colour(split_line[2])
            length = int(split_line[3])
            tunnel_sym = split_line[4]
            loco = int(split_line[5])
            tunnel = False
            if tunnel_sym == "T":
                tunnel = True

            connection = Connection(start, end, colour, length, tunnel, loco)
            city_connection_map[start].append(connection)
            city_connection_map[end].append(connection)
            connections.append(connection)

        if current == routes:
            split_line = line.split(" ")
            start = ab_city_map[split_line[0]]
            end = ab_city_map[split_line[1]]
            value = int(split_line[2])
            route = Route(start, end, value)
            routes.append(route)

    return cities, connections, city_connection_map, routes


def setupMatch(deck: Deck, players, num_starting_cards: int = 3):
    for player in players:
        for i in range(num_starting_cards):
            player.add_to_hand(deck.deal())
