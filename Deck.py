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

        for colour in Colour:
            if colour != Colour.ANY:
                self.__counts[colour] = norm_count
                self.__current_size += norm_count
            else:
                self.__counts[colour] = locomotive_count
                self.__current_size += locomotive_count

        self.updateBoard()

    @property
    def size(self):
        return self.__current_size

    @property
    def board(self):
        return self.__board[:]

    def updateBoard(self):
        num_needed = 5 - len(self.__board)

        for i in range(num_needed):
            new = self.deal()
            if new == Colour.ANY:
                self.__num_loco += 1

            if self.__num_loco >= 3:
                self.__board = []
                self.__num_loco = 0
                self.updateBoard()
            else:
                self.__board.append(new)

    def getFromBoard(self, colour):
        self.__board.remove(colour)
        self.updateBoard()

    def deal(self):
        num = random.randint(0, self.__current_size)
        total = 0

        for colour in Colour:
            total += self.__counts[colour]
            if total > num:
                self.__counts[colour] -= 1
                self.__current_size -= 1
                break

        if self.__current_size == 0:
            self.__reAddDiscarded()

        return colour

    def discard(self, colour, number):
        self.__discarded[colour] += number

    def __reAddDiscarded(self):
        for i in range(len(self.__discarded)):
            self.__current_size += self.__discarded[i]
            self.__current[i] += self.__discarded[i]
            self.__discarded[i] = 0

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
