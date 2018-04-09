import random

class Grid(object):

    ROWS = 4
    COLUMNS = 4

    def __init__(self):
        self.grid = [[0 for x in range(self.COLUMNS)] for y in range(self.ROWS)]

    def __str__(self):
        out = ''
        for y in range(self.ROWS):
            for x in range(self.COLUMNS):
                out = out + str(self.grid[y][x])
            if y != self.ROWS - 1:
                out = out + '\n'
        return out

    @staticmethod
    def random_number():
        return random.sample(2, 4)

    def start_game(self):
        rand_row1 = random.randint(0, self.ROWS)
        rand_row2 = random.randint(0, self.ROWS)
        rand_column1 = random.randint(0, self.COLUMNS)
        rand_column2 = random.randint(0, self.COLUMNS)
        # Make sure that coords are not the same
        while rand_row1 == rand_row2 and rand_column1 == rand_column2:
            rand_row2 = random.randint(0, self.ROWS)
            rand_column2 = random.randint(0, self.COLUMNS)
        self.grid[rand_row1][rand_column1] = self.random_number()
        self.grid[rand_row2][rand_column2] = self.random_number()

        print(str(self))

