import math
from blessings import Terminal


class Renderer():
    cell_width = 7
    cell_height = 3

    def __init__(self, game):
        self.term = Terminal()
        self.game = game

    def _draw_cell(self, x, y, color, values=None):
        x_mid = math.floor(self.cell_width/2)
        y_mid = math.floor(self.cell_height/2)

        for i in range(self.cell_width):
            for j in range(self.cell_height):
                char = ' '
                if values is not None:
                    if i == x_mid and j == 0:
                        char = values[0]
                    elif j == y_mid and i == self.cell_width-1:
                        char = values[1]
                    elif i == x_mid and j == self.cell_height-1:
                        char = values[2]
                    elif j == y_mid and i == 0:
                        char = values[3]
                print(self.term.move(y+j, x+i) + self.term.on_color(color) + '{}'.format(char) + self.term.normal)

    def render(self):
        print(self.term.clear())
        self._render_board()
        self._render_cards()

    def _render_board(self):
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                card = self.game.board[row][col]
                if card is None:
                    color = 250 if (row + col) % 2 == 0 else 253
                    values = None
                else:
                    color = card.player.color
                    values = card.values
                self._draw_cell(row * self.cell_width, col * self.cell_height, color, values=values)

    def _render_cards(self):
        padding = 1
        y = self.cell_height * self.game.rows
        cell_mid = math.floor(self.cell_width/2)
        for i, player in enumerate(self.game.players):
            y += padding
            print(self.term.move(y, 0) + 'Player {}'.format(i+1))
            y += 1
            for j, card in enumerate(player.unplayed_cards):
                self._draw_cell(j * (self.cell_width + 1), y, player.color, card.values)
                print(self.term.move(y + self.cell_height, j * (self.cell_width + 1) + cell_mid) + str(j))
            y += self.cell_height + 1