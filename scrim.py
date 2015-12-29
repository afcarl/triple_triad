from triple_triad import Game
from triple_triad.ai import AIPlayer

n_matches = 100

if __name__ == '__main__':
    players = [
        AIPlayer(228, 'Charles', 'baseline'),
        AIPlayer(216, 'Charlie', 'random')
    ]

    win_loss = {p.name:0 for p in players}

    for _ in range(n_matches):
        winner = Game().play(players, render=False)
        win_loss[winner.name] += 1

    print(win_loss)
