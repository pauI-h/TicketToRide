from unittest import TestCase, mock
from unittest.mock import MagicMock

from Colour import Colour
from Deck import Deck


class Test_Deck(TestCase):

    def setUp(self) -> None:
        self.deck = Deck(100, 100)

    @mock.patch.object(Deck, "updateBoard")
    def testInitialSize(self, updateBoardMock: MagicMock):
        # Uses mock to prevent board assignment affecting size
        deck = Deck(100, 100)
        assert deck.size == 900, deck.size

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
            if deck.count <= 1:
                return Colour.ANY
            else:
                return Colour.YELLOW

        deck.deal = countDeal

        assert deck.board.count(Colour.ANY) == 2
        assert deck.count == 0

        while board.count(Colour.ANY) == 2:
            deck.count = 0 # Accounts for first element being the any
            deck.getFromBoard(board[0])
            board = deck.board
            size -= 1

        assert board == [Colour.YELLOW] * 5, board

    @mock.patch.object(Deck, "_Deck__reAddDiscarded")
    def testReAddDiscardedCards(self, reAddDiscarded_mock: MagicMock):
        deck = Deck(1, 1)

        count = 0
        while deck.size > 1:
            deck.discard(deck.deal(), 1)
            count += 1

        deck.deal()

        reAddDiscarded_mock.assert_called()

    @mock.patch.object(Deck, "discard")
    def testDiscardCardsWhenClearBoard(self, discardMock: MagicMock):

        deck = Deck(10, 30)

        deck.deal = MagicMock(return_value=Colour.YELLOW)

        for i in range(5):
            board = deck.board
            deck.getFromBoard(board[0])

        print(deck.board)

        deck.deal = MagicMock(return_value=Colour.ANY)
        board = deck.board

        while board.count(Colour.ANY) < 2:
            print(deck.board)
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
            deck.count = 0 # Accounts for first element being the any
            deck.getFromBoard(board[0])
            board = deck.board
            size -= 1

        discardMock.assert_called()

    def testReAddDiscardedSize(self):
        deck = Deck(1, 0)
        deck.discard(Colour.YELLOW, 1)
        while deck.size != 1:
            deck.deal()
        deck.deal()
        assert deck.size == 1, deck.size

    def testReAddDiscardedColour(self):
        deck = Deck(1, 0)
        deck.discard(Colour.YELLOW, 1)

        while deck.size != 1:
            deck.deal()
        assert deck.size == 1
        deck.deal()
        assert deck.size == 1

        card = deck.deal()
        assert card == Colour.YELLOW, card
