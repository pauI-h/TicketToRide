import random

from Colour import Colour


class Deck:

    def __init__(self, norm_count, locomotive_count):
        self.__current = []
        self.__board = []
        self.__num_loco = 0
        self.__discarded = {}
        self.__counts = {}
        self.__current_size = 0

        for colour in Colour:  # Sets the beginning number of cards
            if colour != Colour.ANY:
                self.__counts[colour] = norm_count
                self.__current_size += norm_count
            else:
                self.__counts[colour] = locomotive_count
                self.__current_size += locomotive_count
            self.__discarded[colour] = 0

        self.updateBoard()  # Ensures the board is filled

    @property
    def size(self):
        """
        The current number of cards in the deck
        :return:
        """
        return self.__current_size

    @property
    def board(self):
        """
        The current board for cards to be selected from
        :return:
        """
        return self.__board[:]

    def updateBoard(self):
        """
        Updates the board to ensure it is filled
        :return:
        """
        num_needed = 5 - len(self.__board)  # Finds the number of board cards needed

        for i in range(num_needed):
            new = self.deal()
            if new == Colour.ANY:  # Tracks number of locos in board
                self.__num_loco += 1

            if self.__num_loco >= 3:
                self.__board = []  # TODO Replace with discard
                self.__num_loco = 0
                self.updateBoard()
                break  # Stops double growing the board
            else:
                self.__board.append(new)

    def getFromBoard(self, colour) -> None:
        """
        Gets a card from the specified colour from the board
        :param colour: The colour to take
        :return: None
        """
        self.__board.remove(colour)
        self.updateBoard()

    def deal(self):
        """
        Gets a single card from the deck
        :return: The colour of the card
        """
        num = random.randint(0, self.__current_size)
        total = 0

        colour = None  # Fixes warning message
        for colour in Colour:  # Counts until it finds the colour which contains the number
            total += self.__counts[colour]
            if total >= num:
                self.__counts[colour] -= 1
                self.__current_size -= 1
                break

        if self.__current_size == 0:  # Adds discarded cards when needed
            self.__reAddDiscarded()

        return colour

    def discard(self, colour, number):
        """
        Adds cards to the discard pile
        :param colour: The colour to discard
        :param number: The number of cards to discard
        :return:
        """
        self.__discarded[colour] += number

    def __reAddDiscarded(self):
        """
        Adds the discarded cards back into the deck
        :return:
        """
        for colour in Colour:
            count = self.__discarded[colour]
            self.__counts[colour] += count
            self.__current_size += count
            self.__discarded[colour] = 0

    def __str__(self):
        out = ""
        for colour in Colour:
            out += str(colour)
            out += ": "
            out += str(self.__counts[colour])
            out += ", "
        out = out.strip(", ")
        out += ". Board = "
        for card in self.__board:
            out += str(card) + ",  "
        out.strip(", ")
        return out
