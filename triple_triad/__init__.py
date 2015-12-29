from random import shuffle
from .render import Renderer
from .models import Board, Player
from .ai import AIPlayer


class Game():
    """Triple Triad, with the plus, minus, same, and combo rules"""

    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.board = Board(rows, cols)
        self.players = [Player(228), AIPlayer(216)]
        self.cards = sum([p.cards for p in self.players], [])

        # random player goes first
        shuffle(self.players)

        self.renderer = Renderer(self)
        self.winner = None

    def play_card(self, card, x, y):
        if x >= self.cols or y >= self.rows:
            raise Exception("Invalid board position")
        elif self.board[x, y] is not None:
            raise Exception("Cannot place on an occupied space")
        self.board[x, y] = card
        card.played = True
        for changed_card in self.resolve_around(card, x, y):
            changed_card.player = card.player

    def resolve_around(self, card, x, y):
        """compute which cards change ownership for a card played at x,y"""
        changed_cards = []

        # look at adjacent cards
        values_to_compare = []
        if x > 0:
            pos = x-1, y
            adj_card = self.board[pos]
            if adj_card is not None and adj_card.player != card.player:
                values_to_compare.append((pos, card.left, adj_card.right))
        if x < self.cols - 1:
            pos = x+1, y
            adj_card = self.board[pos]
            if adj_card is not None and adj_card.player != card.player:
                values_to_compare.append((pos, card.right, adj_card.left))
        if y > 0:
            pos = x, y-1
            adj_card = self.board[pos]
            if adj_card is not None and adj_card.player != card.player:
                values_to_compare.append((pos, card.top, adj_card.bottom))
        if y < self.rows - 1:
            pos = x, y+1
            adj_card = self.board[pos]
            if adj_card is not None and adj_card.player != card.player:
                values_to_compare.append((pos, card.bottom, adj_card.top))

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
                    changed_cards.extend(self.resolve_around(card, *pos))
                return changed_cards

        # otherwise, compare values
        for pos, this, other in values_to_compare:
            if this > other:
                changed_cards.append(self.board[pos])
        return changed_cards

    def play(self):
        turn = 0
        ai_strategy = None
        self.renderer.render()

        while ai_strategy is None:
            print('Choose AI strategy: {}'.format(AIPlayer.strategies))
            ai_strategy = input('AI strategy:')
            if ai_strategy not in AIPlayer.strategies:
                ai_strategy = None


        while self.winner is None:
            p_idx = turn % 2
            player = self.players[p_idx]
            print('\n{}\'s turn:'.format(player))

            if isinstance(player, AIPlayer):
                print("Thinking...")
                card, x, y = player.decide(ai_strategy, self)
                self.play_card(card, x, y)

            else:
                card_idx = int(input('Card #:'))
                if card_idx >= len(player.unplayed_cards):
                    print('Error: Invalid card index')
                    continue
                x = int(input('x:'))
                y = int(input('y:'))
                card = player.unplayed_cards[card_idx]

                try:
                    self.play_card(card, x, y)
                except Exception as e:
                    print('Error:', str(e))
                    continue

            # check winner
            if turn == self.rows * self.cols - 1:
                self.winner = max(self.players, key=lambda p: len([c for c in self.cards if c.player == p]))

            turn += 1
            self.renderer.render()
        print('Winner: {}'.format(self.winner))
