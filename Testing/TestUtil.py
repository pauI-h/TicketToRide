from Colour import Colour


def placeConnection(player, connection):
    length = connection.getLength()
    for i in range(length):
        player.add_to_hand(Colour.YELLOW)
    player.placeTrain(connection, Colour.YELLOW)