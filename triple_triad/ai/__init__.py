"""
todo:

- BFS
- DFS
- iterative deepening
- uniform cost search
- greedy search
- A*
- minimax
- alpha-beta
- expectimax/expectiminimax
- markov decision process
"""

import random
from ..models import Player


class AIPlayer(Player):
    strategies = ['baseline', 'random']

    def __init__(self, color, name, strategy=None):
        self.strategy = strategy
        super().__init__(color, name)

    def decide(self, game):
        return getattr(self, self.strategy)(game)

    def baseline(self, game):
        """find the weakest card that will win the most cards"""
        candidates = []
        max_wins = 0
        for card in self.unplayed_cards:
            for r, c in game.board.open_positions():
                n_changed = len(game.resolve_around(card, r, c))
                if n_changed > max_wins:
                    candidates = []
                    max_wins = n_changed
                if n_changed == max_wins:
                    candidates.append((card, r, c))
        if not candidates:
            return self.random(game)
        return min(candidates, key=lambda c: sum(c[0].values))

    def random(self, game):
        """play a random card in a random open position"""
        card = random.choice(self.unplayed_cards)
        x, y = random.choice(game.board.open_positions())
        return card, x, y
