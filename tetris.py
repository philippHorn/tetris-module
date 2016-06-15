"""Simple module for Tetris.
Provides two classes, Shape and Game_Control. Both of these only need one instance.
Shape Class:
    The Shape con be optionally provided as a 2d-List, otherwise it will pick a random one.
    All public methods need access to the game objects grid attribute.

    rotate: Rotate the Shape in clockwise or anticlockwise direction.
    update: Moves shape down one row if possible. Otherwise it will respawn at the top as another
        random shape while changing the games grid to be filled in the positions of the old shape.
        If the new block is inside an already filled block, a GameOver exception is raised.
    move: Move the shape left or right, if possible.
    get_on_screen_pos: return an iterator that yields the position for every block of the shape,
        if it is inside of the screen.
Game_Control Class:
    update: Check if there are filled lines, delete them and update the Score accordingly.
"""
import random
import copy

GAME_HEIGHT = 16
GAME_WIDTH = 16

SHAPES = [
    [[1, 1],
     [1, 1]],

    [[0, 1, 0],
     [1, 1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1, 0],
     [0, 1, 1]]
]

class Shape:
    def __init__(self, matrix = None):
        if not matrix:
            matrix = random.choice(SHAPES)
        self.matrix = matrix
        self.height = len(matrix)
        self.width = len(matrix[0])
        self.pos = [GAME_WIDTH // 2, 0] # position of the top left block

    def rotate(self, clockwise = True):
        """rotate matrix by 90 degrees"""

        # make new matrix with width and height reversed
        new_matrix = [[0 for _ in range(self.height)] for _ in range(self.width)]

        for row_count, row in enumerate(self.matrix):
            for col_count, column in enumerate(row):
                if not clockwise:
                    new_matrix[col_count][row_count] = column
                else:
                    new_matrix[col_count][self.height - row_count - 1] = column
        self.matrix = new_matrix
        self.height = len(self.matrix)
        self.width = len(self.matrix[0])

    def update(self, game_grid):
        if self._collide(game_grid, [self.pos[0], self.pos[1] + 1]):
            self._add_to_gamegrid(game_grid)
            # make this object represent a new figure, positioned at the top
            self.__init__()
            print (self._collide(game_grid, self.pos))
            if self._collide(game_grid, self.pos):
                raise GameOver
        else:
            self.pos[1] += 1

    def move(self, gamegrid, left = True):
        new_pos = [self.pos[0] + 1, self.pos[1]] if left \
            else [self.pos[0] - 1, self.pos[1]]
        in_grid = list(self._get_block_positions(new_pos)) == list(self.get_on_screen_pos(new_pos))
        if not self._collide(gamegrid, new_pos) and in_grid:
            self.pos = new_pos

    def _collide(self, game_grid, pos):
        """checks if the shape collides with any blocks on the matrix"""
        return any(game_grid[position[1]][position[0]] == 1 or position[1] >= GAME_HEIGHT - 1\
                     for position in self.get_on_screen_pos(pos))

    def _add_to_gamegrid(self, game_grid):
        for pos in self.get_on_screen_pos(self.pos):
            game_grid[pos[1]][pos[0]] = 1

    def get_on_screen_pos(self, top_left_pos):
        return (pos for pos in self._get_block_positions(top_left_pos) if self._in_grid(pos))

    def _get_block_positions(self, top_left_pos):
        "get the positions for each block in the figures matrix"

        row_positions = [top_left_pos[1] + y for y in range(self.height)]
        col_positions = [top_left_pos[0] + x for x in range(self.width)]
        for row, row_pos in zip(self.matrix, row_positions):
            for col, col_pos in zip(row, col_positions):
                if col == 1:
                    yield (col_pos, row_pos)

    def _in_grid(self, pos):
        return (0 <= pos[0] < GAME_WIDTH) and (0 <= pos[1] < GAME_HEIGHT)

def convert_pos(pos):
    return [GAME_WIDTH - 1 - pos[0], GAME_HEIGHT - 1 - pos[1]]

class Game_Control:
    def __init__(self):
        self.grid = [[0 for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)]
        self.score = 0
        self.paused = False

    def update(self):
        old_lenght = len(self.grid)

        # filter full rows
        self.grid = [row for row in self.grid if any(col == 0 for col in row)]
        lines_removed = old_lenght - len(self.grid)
        self.score += 100 * lines_removed
        # for each removed line, add empty line to the top
        for _ in range(lines_removed):
            self.grid = [0 for _ in range(GAME_WIDTH)] + self.grid

class GameOver(Exception):
    pass