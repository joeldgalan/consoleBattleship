"""
File:    board.py
Author:  Joel Galan
Description: This file will contain the Board class to be used in battleship.py.
"""

HIT_SYMBOL = 'HH'
MISS_SYMBOL = 'MM'
EMPTY_SYMBOL = '  '
DOWN_STRING = 'd'
RIGHT_STRING = 'r'
CARRIER_STRING = 'Carrier'
BATTLESHIP_STRING = 'Battleship'
SUBMARINE_STRING = 'Submarine'
CRUISER_STRING = 'Cruiser'
DESTROYER_STRING = 'Destroyer'
LIFE_INDEX = 2
SYMBOL_INDEX = 0


class Board:

    def __init__(self, size):
        self.size = size

        self.player_grid = []
        for i in range(size):
            row = []
            row.append(i)
            for j in range(size):
                row.append('  ')
            self.player_grid.append(row)
        self.hit_grid = []
        for i in range(size):
            row = []
            row.append(i)
            for j in range(size):
                row.append('  ')
            self.hit_grid.append(row)

    def in_bounds(self, x, y):
        """
            Checks if shot is in bounds of boards.
        :param x: Int, x-value of board.
        :param y: Int, y-value of board.
        :return [x, y]: List, coordinates of either the original shot, or another shot that has been retaken.
        """
        out_of_bounds = False
        if x >= self.size or x < 0 or y >= self.size or y < 0:
            out_of_bounds = True
        # retakes shot if out of bounds and updates coordinates.
        while out_of_bounds:
            print('Shot off of the grid, give new coordinates. ')
            retry_shot = input('Player 1, Enter x y coordinates to fire: ').split()
            x = retry_shot[0]
            y = retry_shot[1]
            if 0 <= int(x) < self.size and 0 <= int(y) < self.size:
                out_of_bounds = False

        return [x, y]

    def register_shot(self, x, y):
        """
            Checks if shot is valid,
            whether it has already been taken(if so will retake shot), and if it is a hit or miss.
        :param x: Int, x-value of shot.
        :param y: Int, y-value of shot.
        :return [True, [x, y - 1]]: List of boolean and list, shot is a hit and coordinates of original shot.
        :return [False, [x, y - 1]]: List of boolean and list, shot is a miss and coordinates of original shot.
        :return [True, [new_x, new_y - 1]]: List of boolean and list, shot is a hit and coordinates of retaken shot.
        :return [False, [new_x, new_y - 1]]: List of boolean and list, shot is a miss and coordinates of retaken shot.
        """
        # checks if shot has already been taken.
        used_spot = False
        retry = False
        if self.player_grid[x][y] == MISS_SYMBOL:
            print('You have already shot there, and missed.')
            used_spot = True
            retry = True
        elif self.player_grid[x][y] == HIT_SYMBOL:
            print('You have already shot there and hit something. ')
            used_spot = True
            retry = True
        # retakes shot if it has already been taken.
        while used_spot:
            retry_shot = input('Enter x y coordinates to fire: ').split()
            retry_shot = self.in_bounds(int(retry_shot[0]), int(retry_shot[1]))
            new_x = int(retry_shot[0])
            new_y = int(retry_shot[1]) + 1
            if self.player_grid[new_x][new_y] == MISS_SYMBOL:
                print('You have already shot there, and missed.')
            elif self.player_grid[new_x][new_y] == HIT_SYMBOL:
                print('You have already shot there and hit something. ')
            else:
                used_spot = False

        # checks if shot is a hit or miss, returns different coordinates based on whether a shot was retaken.
        if not retry:
            if self.player_grid[x][y] != EMPTY_SYMBOL and self.player_grid[x][y] != MISS_SYMBOL \
                    and self.player_grid[x][y] != HIT_SYMBOL:
                return [True, [x, y - 1]]
            elif self.player_grid[x][y] == EMPTY_SYMBOL:
                return [False, [x, y - 1]]
        elif retry:
            if self.player_grid[new_x][new_y] != EMPTY_SYMBOL and self.player_grid[new_x][new_y] != MISS_SYMBOL \
                    and self.player_grid[new_x][new_y] != HIT_SYMBOL:
                return [True, [new_x, new_y - 1]]
            elif self.player_grid[new_x][new_y] == EMPTY_SYMBOL:
                return [False, [new_x, new_y - 1]]

    def get_board(self, hit_or_miss, ships, coordinates, opponent_board):
        """
            Updates player boards and dictionaries.
        :param hit_or_miss: Boolean, whether the shot was a hit or miss.
        :param ships: Dictionary of non-active player's ships.
        :param coordinates: List, coordinates of shot.
        :param opponent_board: List of lists, non-active player's ship board.
        """
        if hit_or_miss:
            for ship in ships:
                if ships[ship][SYMBOL_INDEX] == opponent_board[int(coordinates[0])][(int(coordinates[1]) + 1)]:
                    ships[ship][LIFE_INDEX] -= 1
                    if ships[ship][LIFE_INDEX] <= 0:
                        print('You sunk the {}!'.format(ship))
                    else:
                        print('You hit the {}!'.format(ship))
            self.hit_grid[int(coordinates[0])][int(coordinates[1]) + 1] = HIT_SYMBOL
            opponent_board[int(coordinates[0])][int(coordinates[1]) + 1] = HIT_SYMBOL
        elif not hit_or_miss:
            print('This shot was a miss!')
            self.hit_grid[int(coordinates[0])][(int(coordinates[1]) + 1)] = MISS_SYMBOL
            opponent_board[int(coordinates[0])][(int(coordinates[1]) + 1)] = MISS_SYMBOL

    def place_ship(self, ship, start_pos, down_right):
        """
            Determines if coordinates are legal for ship placement,
            if its in bounds and doesn't overlap with other ships.
        :param ship: String, name of ship to be placed.
        :param start_pos: List, coordinates of chosen starting point for ship.
        :param down_right: String, "d" or "r", tells which direction ship will be placed.
        :return open_space: Boolean, variable declaring whether ship placement is legal or not.
        """
        # gets length of ship being placed.
        if ship == CARRIER_STRING:
            length = 5
        elif ship == BATTLESHIP_STRING:
            length = 4
        elif ship == CRUISER_STRING or ship == SUBMARINE_STRING:
            length = 3
        elif ship == DESTROYER_STRING:
            length = 2

        open_space = True
        i = 0
        # checks if each required point on grid is in bounds and empty for ship going down.
        if down_right == DOWN_STRING:
            while open_space and i < length:
                # checks if in bounds
                if int(start_pos[0]) + length < len(self.player_grid):
                    # checks if empty
                    if self.player_grid[int(start_pos[0]) + i][int(start_pos[1]) + 1] == EMPTY_SYMBOL:
                        # if both are true then in_bounds will remain True, else will become False.
                        open_space = True
                    else:
                        open_space = False
                else:
                    open_space = False

                i += 1
        # same as above but for ship going right.
        elif down_right == RIGHT_STRING:
            while open_space and i < length:
                if int(start_pos[1]) + length < len(self.player_grid[0]):
                    if self.player_grid[int(start_pos[0])][(int(start_pos[1]) + 1) + i] == '  ':
                        open_space = True
                    else:
                        open_space = False
                else:
                    open_space = False
                i += 1

        return open_space
