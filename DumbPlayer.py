from Player import Player


class DumbPlayer(Player):
    def drawTrainTurn(self, map_rep) -> int:
        pass

    def pickRouteTurn(self, map_rep) -> int:
        pass

    def placeTrainTurn(self, map_rep, connections) -> int:
        pass

    def pickAction(self, map_rep, connections) -> (int, int):
        pass

    def calculateMapRep(self, connections):
        pass

    def drawCardTurn(self, map_rep) -> int:
        pass
