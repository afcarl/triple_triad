from random import shuffle
from .render import Renderer
from .models import Board, Player
from .ai import AIPlayer


class PlayerError(Exception):
    pass


class Game():
    """Triple Triad, with the plus, minus, same, and combo rules"""

    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.board = Board(rows, cols)
        self.renderer = Renderer(self)

    def play_card(self, card, x, y):
        if x >= self.cols or y >= self.rows:
            raise PlayerError("Invalid board position")
        elif self.board[x, y] is not None:
            raise PlayerError("Cannot place on an occupied space")
        self.board[x, y] = card
        card.played = True
        for changed_card in self.resolve_around(card, x, y):
            changed_card.player = card.player

    def _values_to_compare(self, x, y, card, side, seen):
        if side == 'left':
            adj_side = 'right'
            x -= 1
        elif side == 'right':
            adj_side = 'left'
            x += 1
        elif side == 'top':
            adj_side = 'bottom'
            y -= 1
        elif side == 'bottom':
            adj_side = 'top'
            y += 1

        if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
            return None

        pos = x, y
        adj_card = self.board[pos]
        if adj_card is not None and adj_card.player != card.player and adj_card not in seen:
            return pos, getattr(card, side), getattr(adj_card, adj_side)

    def resolve_around(self, card, x, y, seen=[]):
        """compute which cards change ownership for a card played at x,y"""
        changed_cards = []

        # look at adjacent cards
        values_to_compare = []
        for side in ['left', 'right', 'top', 'bottom']:
            to_compare = self._values_to_compare(x, y, card, side, seen)
            if to_compare is not None:
                values_to_compare.append(to_compare)

        if len(values_to_compare) > 1:
            combo_play = False

            # check for SAME plays
            if all(this == other for _, this, other in values_to_compare):
                combo_play = True

            # check for PLUS plays
            elif len(set([this + other for _, this, other in values_to_compare])) == 1:
                combo_play = True

            # check for MINUS plays
            elif len(set([this - other for _, this, other in values_to_compare])) == 1:
                combo_play = True

            if combo_play:
                for pos, this, other in values_to_compare:
                    changed_cards.append(self.board[pos])
                    changed_cards.extend(self.resolve_around(card, *pos, seen + changed_cards))
                return changed_cards

        # otherwise, compare values
        for pos, this, other in values_to_compare:
            if this > other:
                changed_cards.append(self.board[pos])
        return changed_cards

    def play(self, players=None, render=True):
        turn = 0
        winner = None

        if players is None:
            self.players = [
                Player(228, "Human Player"),
                AIPlayer(216, "AI Player")
            ]
        else:
            self.players = players

        # random player goes first
        shuffle(self.players)

        if render: self.renderer.render()

        for player in self.players:
            player.draw_cards()

            # select AI strategies
            if isinstance(player, AIPlayer):
                while player.strategy is None:
                    print('Choose AI strategy: {}'.format(AIPlayer.strategies))
                    player.strategy = input('AI strategy:')
                    if player.strategy not in AIPlayer.strategies:
                        player.strategy = None
        self.cards = sum([p.cards for p in self.players], [])

        while winner is None:
            p_idx = turn % 2
            player = self.players[p_idx]

            if render: print('\n{}\'s turn:'.format(player))

            try:
                if isinstance(player, AIPlayer):
                    if render: print("Thinking...")
                    card, x, y = player.decide(self)
                else:
                    card, x, y = self._human_turn(player)

                self.play_card(card, x, y)
            except PlayerError as e:
                print('Error:', str(e))
                continue

            # check winner
            if turn == self.rows * self.cols - 1:
                winner = self._get_winner()

            turn += 1

            if render: self.renderer.render()

        if render: print('Winner: {}'.format(winner))
        return winner

    def _human_turn(self, player):
        card_idx = int(input('Card #:'))
        if card_idx >= len(player.unplayed_cards):
            raise PlayerError('Error: Invalid card index')
        x = int(input('x:'))
        y = int(input('y:'))
        card = player.unplayed_cards[card_idx]
        return card, x, y

    def _get_winner(self):
        return max(self.players, key=lambda p: len([c for c in self.cards if c.player == p]))
