from Colour import Colour


def placeConnection(player, connection):
    length = connection.getLength()
    for i in range(length):
        player.addToHand(Colour.YELLOW)
    player.placeTrain(connection, Colour.YELLOW)