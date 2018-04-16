import random


class Grid(object):

    SIZE = 4
    MAX_LENGTH = 7

    def __init__(self):
        self.grid = [[0 for x in range(self.SIZE)] for y in range(self.SIZE)]
        self.score = 0

    def __str__(self):
        out = ''
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                out = out + str(self.grid[y][x]).ljust(self.MAX_LENGTH)
            if y != self.SIZE - 1:
                out = out + '\n'
        return out

    @staticmethod
    def random_number():
        """
        In 2048, 1 in 10 new numbers are 4, others are 2
        :return: Random number (2 or 4)
        """
        scale = random.randint(1, 10)
        if scale == 1:
            return 4
        else:
            return 2

    def start_game(self):
        """
        Main gameplay engine
        :return:
        """
        rand_row1 = random.randint(0, self.SIZE - 1)
        rand_row2 = random.randint(0, self.SIZE - 1)
        rand_column1 = random.randint(0, self.SIZE - 1)
        rand_column2 = random.randint(0, self.SIZE - 1)
        # Make sure that coords are not the same
        while rand_row1 == rand_row2 and rand_column1 == rand_column2:
            rand_row2 = random.randint(0, self.SIZE - 1)
            rand_column2 = random.randint(0, self.SIZE - 1)
        self.grid[rand_row1][rand_column1] = self.random_number()
        self.grid[rand_row2][rand_column2] = self.random_number()

        print(str(self))
        while self.check_loss() is False:
            self.move()
            print(str(self))

        print('You died, your score: ' + str(self.score))
        return

    @staticmethod
    def ask_for_direction():
        """
        Simple helper to ask for input (can be changed to suit different input methods)
        :return: direction that user inputted
        """
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

    def merge_all_rows_left(self):
        """
        Merges all rows toward the left
        :return: Number of rows changed
        """
        count = 0
        for x in range(self.SIZE):
            count += self.merge_row_left(x)
        return count

    def merge_all_rows_right(self):
        """
        Merges all rows toward the right
        :return: Number of rows changed
        """
        count = 0
        for x in range(self.SIZE):
            count += self.merge_row_right(x)
        return count

    def merge_all_columns_up(self):
        """
        Merges all columns upwards
        :return: Number of columns changed
        """
        count = 0
        for x in range(self.SIZE):
            count += self.merge_column_up(x)
        return count

    def merge_all_columns_down(self):
        """
        Merges all columns downards
        :return: Number of columns changed
        """
        count = 0
        for x in range(self.SIZE):
            count += self.merge_column_down(x)
        return count

    def merge_row_left(self, row_number):
        """
        Merges a single row left
        :param row_number: Row number that is to be merged
        :return: 1 if changes are made, 0 if no changes are made
        """
        count = 0
        for x in range(self.SIZE - 1):  # 0, 1, 2
            if self.grid[row_number][x] != 0:
                for y in range(1, self.SIZE - x):  # if x0: 1-3, if x2: 1
                    if self.grid[row_number][x] == self.grid[row_number][x + y]:
                        self.grid[row_number][x] = self.grid[row_number][x] * 2
                        self.grid[row_number][x + y] = 0
                        self.score += self.grid[row_number][x]
                        count = 1
                        break
                    elif self.grid[row_number][x + y] != 0 and \
                            self.grid[row_number][x] != self.grid[row_number][x + y]:
                        break
        return count

    def merge_column_up(self, column_number):
        """
        Merges a single column up
        :param column_number: Column number that is to be merged
        :return: 1 if changes are made, 0 if no changes are made
        """
        count = 0
        for x in range(self.SIZE - 1):
            if self.grid[x][column_number] != 0:
                for y in range(1, self.SIZE - x):
                    if self.grid[x][column_number] == self.grid[x + y][column_number]:
                        self.grid[x][column_number] = self.grid[x][column_number] * 2
                        self.grid[x + y][column_number] = 0
                        self.score += self.grid[x][column_number]
                        count = 1
                        break
                    elif self.grid[x + y][column_number] != 0 and \
                            self.grid[x][column_number] != self.grid[x + y][column_number]:
                        break
        return count

    def merge_column_down(self, column_number):
        """
        Merges a single column down
        :param column_number: Column number that is to be merged
        :return: 1 if changes are made, 0 if no changes are made
        """
        count = 0
        for x in reversed(range(1, self.SIZE)):  # 3, 2, 1
            if self.grid[x][column_number] != 0:
                for y in range(1, x + 1):  # if x3: 1-3; if x1: 1
                    if self.grid[x][column_number] == self.grid[x - y][column_number]:
                        self.grid[x][column_number] = self.grid[x][column_number] * 2
                        self.grid[x - y][column_number] = 0
                        self.score += self.grid[x][column_number]
                        count = 1
                        break
                    elif self.grid[x - y][column_number] != 0 and \
                            self.grid[x][column_number] != self.grid[x - y][column_number]:
                        break
        return count

    def merge_row_right(self, row_number):
        """
        Merges a single row right
        :param row_number: Row number that is to be merged
        :return: 1 if changes are made, 0 if no changes are made
        """
        count = 0
        for x in reversed(range(1, self.SIZE)):
            if self.grid[row_number][x] != 0:
                for y in range(1, x + 1):
                    if self.grid[row_number][x] == self.grid[row_number][x - y]:
                        self.grid[row_number][x] = self.grid[row_number][x] * 2
                        self.grid[row_number][x - y] = 0
                        self.score += self.grid[row_number][x]
                        count = 1
                        break
                    elif self.grid[row_number][x - y] != 0 and \
                            self.grid[row_number][x] != self.grid[row_number][x - y]:
                        break
        return count

    def move_up(self):
        """
        Moves all numbers in the grid to the up-most position
        :return: 1 if changes are made, 0 if no changes are made
        """
        count = 0
        # For each column: up
        # Starting from 2nd most 'up' part (smallest)
        for y in range(self.SIZE):
            for x in range(1, self.SIZE):
                if self.grid[x][y] != 0:
                    # Keep checking upwards until does not exist or hits a number
                    for z in range(1, x + 1):
                        if x - z == 0 and self.grid[x - z][y] == 0:
                            self.grid[0][y] = self.grid[x][y]
                            self.grid[x][y] = 0
                            count = 1
                            break
                        elif self.grid[x - z][y] != 0 and z != 1:
                            self.grid[x - (z - 1)][y] = self.grid[x][y]
                            self.grid[x][y] = 0
                            count = 1
                            break
                        elif self.grid[x - z][y] != 0:
                            break
        return count

    def move_down(self):
        """
        Moves all numbers in the grid to the down-most position
        :return: 1 if changes are made, 0 if no changes are made
        """
        count = 0
        # For each column: down
        # Starting from 2nd most 'down' part (down)
        for y in range(self.SIZE):
            for x in reversed(range(self.SIZE - 1)):
                if self.grid[x][y] != 0:
                    # Keep checking downwards until does not exist or hits a number
                    for z in range(1, self.SIZE - x):
                        if x + z == self.SIZE - 1 and self.grid[x + z][y] == 0:
                            self.grid[self.SIZE - 1][y] = self.grid[x][y]
                            self.grid[x][y] = 0
                            count = 1
                            break
                        elif self.grid[x + z][y] != 0 and z != 1:
                            self.grid[x + (z - 1)][y] = self.grid[x][y]
                            self.grid[x][y] = 0
                            count = 1
                            break
                        elif self.grid[x + z][y] != 0:
                            break
        return count

    def move_left(self):
        """
        Moves all numbers in the grid to the left-most position
        :return: 1 if changes are made, 0 if no changes are made
        """
        count = 0
        # For each row (x)
        # Starting from 2nd most 'left' part (smallest) (column) (y)
        for x in range(self.SIZE):
            for y in range(1, self.SIZE):
                if self.grid[x][y] != 0:
                    # Keep checking left until does not exist or hits a number
                    for z in range(1, y + 1):
                        if y - z == 0 and self.grid[x][y - z] == 0:
                            self.grid[x][0] = self.grid[x][y]
                            self.grid[x][y] = 0
                            count = 1
                            break
                        elif self.grid[x][y - z] != 0 and z != 1:
                            self.grid[x][y - (z - 1)] = self.grid[x][y]
                            self.grid[x][y] = 0
                            count = 1
                            break
                        elif self.grid[x][y - z] != 0:
                            break
        return count

    def move_right(self):
        """
        Moves all numbers in the grid to the right-most position
        :return: 1 if changes are made, 0 if no changes are made
        """
        count = 0
        # For each row (x)
        # Starting from 2nd most 'right' part (largest) (column) (y)
        for x in range(self.SIZE):
            for y in reversed(range(self.SIZE - 1)):
                if self.grid[x][y] != 0:
                    # Keep checking right until does not exist or hits a number
                    for z in range(1, self.SIZE - y):
                        if y + z == self.SIZE - 1 and self.grid[x][y + z] == 0:
                            self.grid[x][self.SIZE - 1] = self.grid[x][y]
                            self.grid[x][y] = 0
                            count = 1
                            break
                        elif self.grid[x][y + z] != 0 and z != 1:
                            self.grid[x][y + (z - 1)] = self.grid[x][y]
                            self.grid[x][y] = 0
                            count = 1
                            break
                        elif self.grid[x][y + z] != 0:
                            break
        return count

    def move(self):
        """
        Depending on input, moves grid up, down, left or right.
        Then if board changed at all, add a random number at a random empty space.
        :return:
        """
        direction = self.ask_for_direction()
        count = 0
        if direction == 'up':
            count += self.merge_all_columns_up()
            count += self.move_up()
        elif direction == 'down':
            count += self.merge_all_columns_down()
            count += self.move_down()
        elif direction == 'left':
            count += self.merge_all_rows_left()
            count += self.move_left()
        elif direction == 'right':
            count += self.merge_all_rows_right()
            count += self.move_right()
        # Invalid move if count == 0
        if count != 0:
            self.random_number_at_a_space()
        return

    def random_number_at_a_space(self):
        """
        Puts a random between 2 or 4 at a random empty square
        :return:
        """
        storage = []
        for x in range(self.SIZE):
            for y in range(self.SIZE):
                if self.grid[x][y] == 0:
                    storage.append((x, y))
        coords = random.choice(storage)
        self.grid[coords[0]][coords[1]] = self.random_number()
        return

    def check_loss(self):
        """
        Check if game is lost (all grids filled up)
        :return: True/False
        """
        for x in range(self.SIZE):
            for y in range(self.SIZE):
                if self.grid[x][y] == 0:
                    return False
        return True
