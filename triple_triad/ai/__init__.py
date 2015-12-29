"""
todo:

- random
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

implement way of playing many, many games against baseline:

baseline strategy: play to win cards
"""

import random
from time import sleep
from ..models import Player

class AIPlayer(Player):
    strategies = ['baseline', 'random']

    def decide(self, strategy, game):
        sleep(random.randint(1, 2)) # "thinking"
        return getattr(self, strategy)(game)

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
        return card, random.choice(game.board.open_positions())

    def __str__(self):
        return "AI Player"
