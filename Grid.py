import random


class Grid(object):

    ROWS = 4
    COLUMNS = 4
    MAX_LENGTH = 5

    def __init__(self):
        self.grid = [[0 for x in range(self.COLUMNS)] for y in range(self.ROWS)]

    def __str__(self):
        out = ''
        for y in range(self.ROWS):
            for x in range(self.COLUMNS):
                out = out + str(self.grid[y][x]).ljust(self.MAX_LENGTH)
            if y != self.ROWS - 1:
                out = out + '\n'
        return out

    @staticmethod
    def random_number():
        scale = random.randint(1, 10)
        if scale == 1:
            return 4
        else:
            return 2

    def start_game(self):
        rand_row1 = random.randint(0, self.ROWS - 1)
        rand_row2 = random.randint(0, self.ROWS - 1)
        rand_column1 = random.randint(0, self.COLUMNS - 1)
        rand_column2 = random.randint(0, self.COLUMNS - 1)
        # Make sure that coords are not the same
        while rand_row1 == rand_row2 and rand_column1 == rand_column2:
            rand_row2 = random.randint(0, self.ROWS - 1)
            rand_column2 = random.randint(0, self.COLUMNS - 1)
        self.grid[rand_row1][rand_column1] = self.random_number()
        self.grid[rand_row2][rand_column2] = self.random_number()

        print(str(self))
        while self.check_loss() is False:
            self.move()
            print(str(self))

        print('You died, your top number was: ' + str(self.find_score()))

    @staticmethod
    def ask_for_direction():
        while True:
            print('Input WASD for swipe direction')
            direction = input()
            if direction == 'w':
                return 'up'
            elif direction == 'a':
                return 'left'
            elif direction == 's':
                return 'down'
            elif direction == 'd':
                return 'right'
            else:
                print('Please input w,a,s, or d')

    def merge(self, row_or_col, type_number):
        a = 0
        b = 0
        if row_or_col == 'row':
            a = 1
            total = self.ROWS
        else:
            b = 1
            total = self.COLUMNS

        for x in range(total - 1):
            if self.grid[x * b + type_number * a][x * a + type_number * b] == \
                    self.grid[(x + 1) * b + type_number * a][(x + 1) * a + type_number * b]:


                self.grid[x * b + type_number * a][x * a + type_number * b] = \
                    self.grid[x * b + type_number * a][x * a + type_number * b] * 2
                self.grid[(x + 1) * b + type_number * a][(x + 1) * a + type_number * b] = 0
        return

    def move_direction(self, direction):
        if direction == 'up' or direction == 'down':
            first = self.COLUMNS
            second = self.ROWS
            row_col = 'column'
        else:
            first = self.ROWS
            second = self.COLUMNS
            row_col = 'row'

        for y in range(first):
            # self.merge(row_col, y)
            for x in range(1, second):
                if self.grid[x][y] != 0:
                    # Look up one step at a time, check for collisions
                    for z in range(1, x + 1):
                        if self.grid[x - z][y] != 0:
                            self.grid[x - z + 1][y] = self.grid[x][y]
                            if z - 1 != 0:
                                self.grid[y][x] = 0
                            break
                        elif x - z == 0:
                            self.grid[x - z][y] = self.grid[x][y]
                            self.grid[x][y] = 0
                            break

    def move(self):
        direction = self.ask_for_direction()
        # If up: move all pieces to minimum rows
        if direction == 'up':
            # Start from top row
            for y in range(self.COLUMNS):
                # self.merge('column', y)
                for x in range(1, self.ROWS):
                    if self.grid[x][y] != 0:
                        # Look up one step at a time, check for collisions
                        for z in range(1, x + 1):
                            if self.grid[x - z][y] != 0:
                                self.grid[x - z + 1][y] = self.grid[x][y]
                                if z - 1 != 0:
                                    self.grid[y][x] = 0
                                break
                            elif x - z == 0:
                                self.grid[x - z][y] = self.grid[x][y]
                                self.grid[x][y] = 0
                                break

        if direction == 'down':
            # Start from bottom row (largest)
            for y in range(self.COLUMNS):
                # self.merge('column', y)
                for x in range(1, self.ROWS):
                    # Added swap direction
                    x = self.ROWS - 1 - x
                    print(x)
                    if self.grid[x][y] != 0:
                        # Look up one step at a time, check for collisions
                        for z in range(1, self.ROWS - x):
                            if self.grid[x + z][y] != 0:
                                self.grid[x + z - 1][y] = self.grid[x][y]
                                if z - 1 != 0:
                                    self.grid[y][x] = 0
                                break
                            elif x + z == self.ROWS - 1:
                                self.grid[x + z][y] = self.grid[x][y]
                                self.grid[x][y] = 0
                                break

        if direction == 'left':
            # Start from top row
            for y in range(self.ROWS):
                # self.merge('row', y)
                for x in range(1, self.COLUMNS):
                    if self.grid[y][x] != 0:
                        # Look up one step at a time, check for collisions
                        for z in range(1, x + 1):
                            if self.grid[y][x - z] != 0:
                                self.grid[y][x - z + 1] = self.grid[y][x]
                                if z - 1 != 0:
                                    self.grid[y][x] = 0
                                break
                            elif x - z == 0:
                                self.grid[y][x - z] = self.grid[y][x]
                                self.grid[y][x] = 0
                                break

        if direction == 'right':
            # Start from bottom row (largest)
            for y in range(self.ROWS):
                # self.merge('row', y)
                for x in range(1, self.COLUMNS):
                    # Added swap direction
                    x = self.COLUMNS - 1 - x
                    if self.grid[y][x] != 0:
                        # Look up one step at a time, check for collisions
                        for z in range(1, self.COLUMNS - x):
                            if self.grid[y][x + z] != 0:
                                self.grid[y][x + z - 1] = self.grid[y][x]
                                if z - 1 != 0:
                                    self.grid[y][x] = 0
                                break
                            elif x + z == self.COLUMNS - 1:
                                self.grid[y][x + z] = self.grid[y][x]
                                self.grid[y][x] = 0
                                break

        self.random_number_at_a_space()

    def random_number_at_a_space(self):
        storage = []
        for x in range(self.ROWS):
            for y in range(self.COLUMNS):
                if self.grid[x][y] == 0:
                    storage.append((x, y))
        coords = random.choice(storage)
        self.grid[coords[0]][coords[1]] = self.random_number()
        return

    def check_loss(self):
        for x in range(self.ROWS):
            for y in range(self.COLUMNS):
                if self.grid[x][y] == 0:
                    return False
        return True

    def find_score(self):
        score = 0
        for x in range(self.ROWS):
            for y in range(self.COLUMNS):
                if self.grid[x][y] > score:
                    score = self.grid[x][y]
        return score





