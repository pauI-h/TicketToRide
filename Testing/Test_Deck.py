from unittest import TestCase

from Deck import Deck


class Test_Deck(TestCase):

    def setUp(self) -> None:
        self.deck = Deck(100, 100)

    def testInitialSize(self):
        assert self.deck.size == 895, self.deck.size
