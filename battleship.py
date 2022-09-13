"""
File:    battleship.py
Author:  Joel Galan
Description: This file will run the BattleShip game.
"""

from board import Board

MAX_DEATHS_INT = 5
HIT_SYMBOL = 'HH'
MISS_SYMBOL = 'MM'
DOWN_STRING = 'd'
RIGHT_STRING = 'r'
DIRECTION_STRINGS = ['d', 'r']
LIFE_INDEX = 2
SYMBOL_INDEX = 0


class BattleshipGame:
    def __init__(self, size=10):
        self.size = size
        self.p1_ships = {'Carrier': ['Ca', 5, 5], 'Battleship': ['Ba', 4, 4], 'Cruiser': ['Cr', 3, 3],
                         'Submarine': ['Su', 3, 3], 'Destroyer': ['De', 2, 2]}
        self.p1_deaths = 0
        self.p2_ships = {'Carrier': ['Ca', 5, 5], 'Battleship': ['Ba', 4, 4], 'Cruiser': ['Cr', 3, 3],
                         'Submarine': ['Su', 3, 3], 'Destroyer': ['De', 2, 2]}
        self.p2_deaths = 0
        self.player_boards = []

    def run_game(self):
        """
            Runs Battleship game.
        """
        # phase 1, setting up game
        print('Player 1, prepare to place your fleet.')
        p1_board = Board(self.size)
        self.player_boards.append(p1_board)
        self.place_ships(p1_board, self.p1_ships, p1_board.player_grid)
        print('Player 2, prepare to place your fleet.')
        p2_board = Board(self.size)
        self.player_boards.append(p2_board)
        self.place_ships(p2_board, self.p2_ships, p2_board.player_grid)

        # phase 2, playing game
        running_game = True
        while running_game:
            if running_game:
                self.display_boards(1)
                shot = input('Player 1, Enter x y coordinates to fire: ').split()
                # detects if shot is in bounds.
                shot = p1_board.in_bounds(int(shot[0]), int(shot[1]))
                # determines whether shot is a hit or miss.
                hit_miss = p2_board.register_shot(int(shot[0]), int(shot[1]) + 1)
                # updates boards and ship health.
                p1_board.get_board(hit_miss[0], self.p2_ships, hit_miss[1], p2_board.player_grid)

            # checks if ship life values have been depleted/sunk, if yes then adds death to player death count.
            for ship in self.p1_ships:
                if self.p1_ships[ship][LIFE_INDEX] == 0:
                    self.p1_ships[ship][LIFE_INDEX] = -1
                    self.p1_deaths += 1
            for ship in self.p2_ships:
                if self.p2_ships[ship][LIFE_INDEX] == 0:
                    self.p2_ships[ship][LIFE_INDEX] = -1
                    self.p2_deaths += 1

            # checks if a player has lost.
            if self.p1_deaths == MAX_DEATHS_INT or self.p2_deaths == MAX_DEATHS_INT:
                running_game = False

            if running_game:
                self.display_boards(2)
                shot = input('Player 2, Enter x y coordinates to fire: ').split()
                # detects if shot is in bounds.
                shot = p2_board.in_bounds(int(shot[0]), int(shot[1]))
                # determines whether shot is a hit or miss.
                hit_miss = p1_board.register_shot(int(shot[0]), int(shot[1]) + 1)
                # updates boards and ship health.
                p2_board.get_board(hit_miss[0], self.p1_ships, hit_miss[1], p1_board.player_grid)

            # checks if ship life values have been depleted/sunk, if yes then adds death to player death count.
            for ship in self.p1_ships:
                if self.p1_ships[ship][LIFE_INDEX] == 0:
                    self.p1_ships[ship][LIFE_INDEX] = -1
                    self.p1_deaths += 1
            for ship in self.p2_ships:
                if self.p2_ships[ship][LIFE_INDEX] == 0:
                    self.p2_ships[ship][LIFE_INDEX] = -1
                    self.p2_deaths += 1

            # checks if someone has sunken all their opponents' ships, if so then breaks while loop/ends game.
            if self.p1_deaths == MAX_DEATHS_INT or self.p2_deaths == MAX_DEATHS_INT:
                running_game = False

        # announces winner.
        if self.p1_deaths == MAX_DEATHS_INT:
            print('Player 2 has won.')
        elif self.p2_deaths == MAX_DEATHS_INT:
            print('Player 1 has won.')

    def place_ships(self, player, player_ships, player_board):
        """
            Runs first phase of game to set up and place ships on each players board.
        :param player_ships: Dictionary of current player's ships.
        :param player_board: List of lists functioning as current players board, ships will be added into the board.
        """
        # prints numbers at top of board
        print('  ', end='')
        for i in range(len(player_board)):
            if i >= len(player_board) - 1:
                print(i)
            else:
                print(i, end='  ')
        # prints rest of board
        for i in range(len(player_board)):
            for j in range(len(player_board[i])):
                if j == 0:
                    print(player_board[i][j], end=' ')
                elif j >= len(player_board):
                    print(player_board[i][j], end='|\n')
                else:
                    print(player_board[i][j], end='|')

        # asks for player to place their ships, and places them on the board
        for ship in player_ships:
            coordinates = input('Enter x y coordinates to place the {}: '.format(ship)).split()
            d_r = input('Enter Right or Down (r or d): ').strip()
            if d_r not in DIRECTION_STRINGS:
                while d_r not in DIRECTION_STRINGS:
                    d_r = input('Enter Right or Down (r or d): ').strip()
            # checks if shot is legal.
            legal_place = player.place_ship(ship, coordinates, d_r)
            # if not legal will ask for new coordinates and check again.
            while not legal_place:
                print('Invalid position or overlapping ships, try again. ')
                coordinates = input('Enter x y coordinates to place the {}: '.format(ship)).split()
                d_r = input('Enter Right or Down (r or d): ').strip()
                legal_place = player.place_ship(ship, coordinates, d_r)
            # if is legal, will place ship on board.
            if legal_place:
                for i in range(player_ships[ship][1]):
                    if d_r == DOWN_STRING:
                        player_board[int(coordinates[0]) + i][int(coordinates[1]) + 1] = player_ships[ship][SYMBOL_INDEX]
                    elif d_r == RIGHT_STRING:
                        player_board[int(coordinates[0])][(int(coordinates[1]) + 1) + i] = \
                            player_ships[ship][SYMBOL_INDEX]

            # prints starting board.
            # prints top row of numbers
            print('  ', end='')
            for i in range(len(player_board)):
                if i >= len(player_board) - 1:
                    print(i)
                else:
                    print(i, end='  ')
            # prints rest of board
            for i in range(len(player_board)):
                for j in range(len(player_board[i])):
                    if j == 0:
                        print(player_board[i][j], end=' ')
                    elif j >= len(player_board):
                        print(player_board[i][j], end='|\n')
                    else:
                        print(player_board[i][j], end='|')

    def display_boards(self, turn):
        """
            displays player ship and hit boards.
        :param turn: Int, 1 or 2, whose player's turn it is.
        """
        if turn == 1:
            # prints top numbers row
            print('   ', end='')
            for i in range(len(self.player_boards[0].player_grid)):
                if i == len(self.player_boards[0].player_grid) - 1:
                    print(i, end=' \t\t    ')
                else:
                    print(i, end='  ')
            for i in range(len(self.player_boards[0].hit_grid)):
                if i >= len(self.player_boards[0].hit_grid) - 1:
                    print(i)
                else:
                    print(i, end='  ')

            # prints rest of board
            for i in range(len(self.player_boards[0].player_grid)):
                for j in range(len(self.player_boards[0].player_grid[i])):
                    if j == 0:
                        print(' ' + str(self.player_boards[0].player_grid[i][j]), end=' ')
                    else:
                        print(self.player_boards[0].player_grid[i][j], end='|')
                print('\t\t', end=' ')
                for j in range(len(self.player_boards[0].hit_grid[i])):
                    if j == 0:
                        print(' ' + str(self.player_boards[0].hit_grid[i][j]), end=' ')
                    elif j >= len(self.player_boards[0].hit_grid[i]) - 1:
                        print(self.player_boards[0].hit_grid[i][j], end='\n')
                    else:
                        print(self.player_boards[0].hit_grid[i][j], end='|')
                print('|')

        elif turn == 2:
            # prints top numbers row
            print('   ', end='')
            for i in range(len(self.player_boards[1].player_grid)):
                if i == len(self.player_boards[1].player_grid) - 1:
                    print(i, end=' \t\t    ')
                else:
                    print(i, end='  ')
            for i in range(len(self.player_boards[1].hit_grid)):
                if i >= len(self.player_boards[1].hit_grid) - 1:
                    print(i)
                else:
                    print(i, end='  ')

            # prints rest of board
            for i in range(len(self.player_boards[1].hit_grid)):
                for j in range(len(self.player_boards[1].hit_grid[i])):
                    if j == 0:
                        print(' ' + str(self.player_boards[1].player_grid[i][j]), end=' ')
                    else:
                        print(self.player_boards[1].hit_grid[i][j], end='|')
                print('\t\t', end=' ')
                for j in range(len(self.player_boards[1].player_grid[i])):
                    if j == 0:
                        print(' ' + str(j), end=' ')
                    elif j >= len(self.player_boards[1].player_grid[i]) - 1:
                        print(self.player_boards[1].player_grid[i][j], end='\n')
                    else:
                        print(self.player_boards[1].player_grid[i][j], end='|')
                print('|')


if __name__ == "__main__":
    BattleshipGame().run_game()
