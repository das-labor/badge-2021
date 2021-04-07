from emulator import SSD1306_I2C

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 200, 0)

def rng():
    'Return a pseudo random byte value'
    try:
        import os
        # http://docs.micropython.org/en/latest/library/uos.html?highlight=uos#uos.urandom
        os.urandom(1)[0]
    except:
        print('unable to use urandom. Trying other RNG')

    try:
        import random
        return random.randbytes(1)[0]
    except:
        print('Unable to use randbytes')


class GameOfLife:
    """Conway's Game of Life"""

    MAX_ITERATIONS = 100
    INTITIAL_CELL_COVERAGE = 0.2

    def __init__(self):
        self.iterations = 0
        self.oled = SSD1306_I2C()

        self.cells = []
        for x in range(self.oled.width):
            self.cells.append([0] * self.oled.height)

        self.reset()

    def reset(self):
        self.iterations = 0
        for i in range(
            int(self.oled.width * self.oled.height * GameOfLife.INTITIAL_CELL_COVERAGE)):

            x = int(rng() / 255 * (self.oled.width-1))
            y = int(rng() / 255 * (self.oled.height-1))
            self.cells[x][y] = 1

    def _iterate(self):
        new_board = []
        for x in range(gol.oled.width):
            new_board.append([0] * self.oled.height)

        for y in range(self.oled.height):
            for x  in range(self.oled.width):
                num_neighbours = self._neighbours(x,y)

                if self.cells[x][y]==1 and num_neighbours in (2, 3):
                    new_board[x][y] = 1

                elif self.cells[x][y]==0 and num_neighbours==3:
                    new_board[x][y] = 1

                else:
                    new_board[x][y] = 0

        return new_board

    def on_board(self, x, y):
        return 0 <= x < self.oled.width and 0 <= y < self.oled.height

    def _neighbours(self, x,y):
        r = [-1, 0, 1]
        num_neighbours = 0
        for dx,dy in [(i,j) for i in r for j in r if not i == j == 0]:
            if self.on_board(x+dx,y+dy) and self.cells[x+dx][y+dy] == 1:
                num_neighbours += 1

        return num_neighbours

    def prepare(self):
        self.cells = self._iterate()
        self.iterations += 1
        if self.iterations > GameOfLife.MAX_ITERATIONS:
            self.reset()

    def handle_px(self, x, y):
        if self.cells[x][y]==1:
            color = GREEN
        else:
            color = BLACK

        self.oled.pixel(x,y, color)

gol = GameOfLife()

while True:
    gol.prepare()
    for y in range(gol.oled.height):
        for x  in range(gol.oled.width):
            gol.handle_px(x,y)

    gol.oled.fill_rect(0,0, 90, 10, BLACK)
    gol.oled.text(str(gol.iterations) + " - Game Of Life", 0,0, WHITE)
    gol.oled.show()
