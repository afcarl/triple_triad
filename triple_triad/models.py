import random
from .cards import cards


class Board():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[None for c in range(cols)] for r in range(rows)]

    def __getitem__(self, pos):
        x, y = pos
        return self.board[x][y]

    def __setitem__(self, pos, value):
        x, y = pos
        self.board[x][y] = value

    def open_positions(self):
        open_pos = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] is None:
                    open_pos.append((r, c))
        return open_pos


class Player():
    def __init__(self, color, name):
        self.name = name
        self.color = color

    def draw_cards(self):
        self.cards = [Card.random_card() for _ in range(5)]
        for card in self.cards:
            card.player = self

    @property
    def unplayed_cards(self):
        return [c for c in self.cards if not c.played]

    def __str__(self):
        return self.name


class Card():
    @staticmethod
    def random_card():
        return Card(random.choice(cards))

    def __init__(self, values):
        self.values = values
        self.played = False

        # for convenience
        self.top, self.right, self.bottom, self.left = values
