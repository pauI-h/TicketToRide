import random

from Colour import Colour


class Deck:

    def __init__(self, norm_count, locomotive_count):
        self.__current = []
        self.__board = []
        self.__colour_pos_map = {}
        self.__pos_colour_map = {}
        self.__num_loco = 0
        self.__discarded = []
        i = 0

        for colour in Colour:
            self.__colour_pos_map[colour] = i
            self.__pos_colour_map[i] = colour
            self.__discarded.append(0)
            if colour != Colour.ANY:
                self.__current.append(norm_count)
            else:
                self.__current.append(locomotive_count)
            i += 1

        self.__current_size = sum(self.__current)
        self.update_board()

    def getColourPosMap(self):
        return self.__colour_pos_map

    def showBoard(self):
        return self.__board[:]

    def update_board(self):
        num_needed = 5 - len(self.__board)
        for i in range(num_needed):
            new = self.deal()
            if new == Colour.ANY:
                self.__num_loco += 1

            if self.__num_loco >= 3:
                self.__board = []
                self.__num_loco = 0
                self.update_board()
            else:
                self.__board.append(new)

    def getFromBoard(self, colour):
        self.__board.remove(colour)
        self.update_board()

    def deal(self):
        num = random.randint(0, self.__current_size)
        total = 0
        for colour in Colour:
            total += self.__current[self.__colour_pos_map[colour]]
            if total > num:
                break
        self.__current[self.__colour_pos_map[colour]] -= 1
        self.__current_size -= 1
        return colour

    def discard(self, colour):
        self.__discarded[self.__colour_pos_map[colour]] += 1

    def re_add_discarded(self):
        for i in range(len(self.__discarded)):
            self.__current[i] += self.__discarded[i]
            self.__discarded[i] = 0

    def __str__(self):
        out = ""
        for colour in Colour:
            out += str(colour)
            out += ": "
            out += str(self.__current[self.__colour_pos_map[colour]])
            out += ", "
        out = out.strip(", ")
        out += ". Board = "
        for card in self.__board:
            out += str(card) + ",  "
        out.strip(", ")
        return out
