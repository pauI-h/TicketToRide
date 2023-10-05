from unittest import TestCase

from Colour import Colour
from Deck import Deck
from Players.TestPlayer import TestPlayer


class Test_Player(TestCase):

    def testAddToHand(self):
        player = TestPlayer(100, 100, Deck(1, 1))
        player.addToHand(Colour.RED)
        hand = player.hand.copy()
        assert hand[Colour.RED] == 1


