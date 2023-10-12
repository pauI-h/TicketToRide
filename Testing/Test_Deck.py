from unittest import TestCase
from unittest.mock import MagicMock

from Colour import Colour
from Deck import Deck


class Test_Deck(TestCase):

    def setUp(self) -> None:
        self.deck = Deck(100, 100)

    def testInitialSize(self):
        assert self.deck.size == 895, self.deck.size

    def testBoardSize(self):
        assert len(self.deck.board) == 5

    def testBoardSizeAfterTake(self):
        c = self.deck.board[0]
        self.deck.getFromBoard(c)
        assert len(self.deck.board) == 5

    def testBoardResetAfterThreeLocos(self):
        deck = Deck(10, 30)
        deck.deal = MagicMock(return_value=Colour.ANY)
        board = deck.board
        while board.count(Colour.ANY) < 2:
            deck.getFromBoard(board[0])
            board = deck.board
        size = deck.size
        deck.count = 0

        def countDeal():
            deck.count += 1
            if deck.count == 1:
                return Colour.ANY
            else:
                return Colour.YELLOW

        deck.deal = countDeal

        while board.count(Colour.ANY) == 2:
            deck.getFromBoard(board[0])
            board = deck.board
            size -= 1

        assert board == [Colour.YELLOW]*5
