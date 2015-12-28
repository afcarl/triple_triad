from random import randint, shuffle
from .render import Renderer


class Game():
    """Triple Triad, with the plus, minus, same, and combo rules"""

    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.board = [[None for c in range(self.cols)] for r in range(self.rows)]
        self.players = [
            Player(206, [Card.random_card() for _ in range(5)]),
            Player(220, [Card.random_card() for _ in range(5)])
        ]
        # random player goes first
        shuffle(self.players)

        self.renderer = Renderer(self)
        self.winner = None

    def play_card(self, card, x, y):
        if x >= self.cols or y >= self.rows:
            raise Exception("Invalid board position")
        elif self.board[x][y] is not None:
            raise Exception("Cannot place on an occupied space")
        self.board[x][y] = card
        card.played = True
        self._resolve_around(x, y)

    def _resolve_around(self, x, y):
        card = self.board[x][y]

        # look at adjacent cards
        values_to_compare = []
        if x > 0:
            adj_card = self.board[x-1][y]
            if adj_card is not None and adj_card.player != card.player:
                values_to_compare.append(((x-1, y), card.left, adj_card.right))
        if x < self.cols - 1:
            adj_card = self.board[x+1][y]
            if adj_card is not None and adj_card.player != card.player:
                values_to_compare.append(((x+1, y), card.right, adj_card.left))
        if y > 0:
            adj_card = self.board[x][y-1]
            if adj_card is not None and adj_card.player != card.player:
                values_to_compare.append(((x, y-1), card.top, adj_card.bottom))
        if y < self.rows - 1:
            adj_card = self.board[x][y+1]
            if adj_card is not None and adj_card.player != card.player:
                values_to_compare.append(((x, y+1), card.bottom, adj_card.top))

        if len(values_to_compare) > 1:
            combo_play = False

            # check for SAME plays
            if all(this == other for pos, this, other in values_to_compare):
                combo_play = True

            # check for PLUS plays
            elif len(set([this + other for pos, this, other in values_to_compare])) == 1:
                combo_play = True

            # check for MINUS plays
            elif len(set([this - other for pos, this, other in values_to_compare])) == 1:
                combo_play = True

            if combo_play:
                for (x_, y_), this, other in values_to_compare:
                    self.board[x_][y_].player = card.player
                    self._resolve_around(x_,y_)
                return

        # otherwise, compare values
        for (x_, y_), this, other in values_to_compare:
            if this > other:
                self.board[x_][y_].player = card.player

    def play(self):
        turn = 0
        self.renderer.render()
        while self.winner is None:
            p_idx = turn % 2
            print('\nPlayer {}\'s turn:'.format(p_idx+1))
            card_idx = int(input('Card #:'))
            if card_idx >= len(self.players[p_idx].unplayed_cards):
                print('Error: Invalid card index')
                continue
            x = int(input('x:'))
            y = int(input('y:'))
            card = self.players[p_idx].unplayed_cards[card_idx]

            try:
                self.play_card(card, x, y)
            except Exception as e:
                print('Error:', str(e))
                continue
            turn += 1
            self.renderer.render()


class Player():
    def __init__(self, color, cards):
        self.color = color
        self.cards = cards
        for card in self.cards:
            card.player = self

    @property
    def unplayed_cards(self):
        return [c for c in self.cards if not c.played]


class Card():
    @staticmethod
    def random_card():
        return Card(
            (randint(1, 9), randint(1, 9), randint(1, 9), randint(1, 9))
        )

    def __init__(self, values):
        self.values = values
        self.played = False

        # for convenience
        self.top, self.right, self.bottom, self.left = values
