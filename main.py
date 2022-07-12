"""
File: WaveFunctionCollapse - Sudoku
Author: Christopher Kihano
Date: July 12 2022
Description:
             Solver for 2D square sudoku boards of size n^2 using branching and backtracking. Used as a practice for
             learning how to use wave function collapse. Wave function collapse takes all possible values that a cell
             can take on, and using the rules provided, reduces the possible values that cell can take on. If there's
             only one possible solution for a cell, the cell is determined to be that value. However, if there are no
             cells with only one solution and instead have multiple solutions, a branch is taken with one of the
             possible values and further reductions are made with that assumption. Either the guess is correct and will
             produce a correct solution or there will be a cell with no solution in which the board is unsolvable. If
             the board becomes unsolvable, the program will backtrack to where the last choice was made, and take the
             other route. If all routes are exhausted along a branch, it will backtrack further to the previous branch
             in which the board still has a possibility of being solved given a different choice.

Further Improvements:
            Looking at other solvers after completing my own, I see what looks to be simpler implementations. However,
            these also seem to use a more brute force method in which all possible values are tried in a cell until a
            no solution cell is found and then backtracking is performed. Should I return to this, I may look more into
            how they solved this problem further, but I'm happy with my solution. They also assume 9x9 boards.
"""

import copy
import math


class Board:
    def __init__(self, board: list[list], possible_values: list):
        """ Board class for passing around board instances and printing and solving boards.

        :param board: A 2D array of the board. 0 denotes unsolved, a list is possible values, others are given values.
        :param possible_values: List of possible values each cell can take on. This includes numbers, letters, objects.

        """
        self.board = copy.deepcopy(board)
        self.width = len(board)
        self.height = len(board[0])
        for y in range(self.height):
            for x in range(self.width):
                self.board[x][y] = copy.deepcopy(possible_values) if not board[x][y] else board[x][y]
        self.sub_block = int(math.sqrt(self.width))
        self.return_line_string = " ".join(["{" + str(i) + ":3}" for i in range(self.width)]) + '\n'

    def __str__(self):
        return_string = ""
        for row in self.board:
            return_string += self.return_line_string.format(*[str(item) for item in row])
        return return_string

    def reduce_entropy(self) -> tuple[int, list[int], list]:
        """
        Checks the board, cell by cell, to determine if the entropy of the cell can be reduced. If a cell has an
        entropy of 0, an incorrect route was taken. If a cell has an entropy of 1, then for that particular route,
        there's only one possible value and that value is placed in that cell. As the cells are being iterated over to
        determine entropy, the cell with the lowest entropy is recorded. If the entropy is two or more, a guess must be
        made between the possible values.
        :return: Lowest entropy of all the cells, where that cell is located, what possible values that cell can have.
        """
        lowest_entropy = 9  # Using 9 as a marker for no possible moves could be made.
        location = [0, 0]  # Default using 0, 0 as return statements wants not None values
        for y, row in enumerate(self.board):  # Grab the row as an object for next line but also offset
            for x, cell in enumerate(row):
                if isinstance(cell, list):  # Only run this code if there's unsolved cells in board instance
                    # Check horizontal rows
                    for j in range(self.width):
                        if not isinstance(self.board[y][j], list) and self.board[y][j] in cell:
                            cell.remove(self.board[y][j])
                        if not isinstance(self.board[j][x], list) and self.board[j][x] in cell:
                            cell.remove(self.board[j][x])
                    # Check sub-squares
                    top_left_x = (x // self.sub_block) * self.sub_block  # Top left x of sub-squares
                    top_left_y = (y // self.sub_block) * self.sub_block  # Same but y
                    for box_y in range(top_left_y, top_left_y + self.sub_block):  # Scan sub-square to find solved cells
                        for box_x in range(top_left_x, top_left_x + self.sub_block):
                            if not isinstance(self.board[box_y][box_x], list) and self.board[box_y][box_x] in cell:
                                cell.remove(self.board[box_y][box_x])  # Remove from the list the value in board[y][x]
                    # Determine entropy after removing already filled values
                    num_elements_in_cell = len(cell)
                    # If there's only one possible choice for the given board instance, apply choice
                    if num_elements_in_cell == 1:
                        self.board[y][x] = self.board[y][x][0]
                    # Keep track of what cell has the lowest entropy for use in making splits
                    if num_elements_in_cell < lowest_entropy:
                        lowest_entropy = num_elements_in_cell
                        location = [y, x]
        return lowest_entropy, location, self.board[location[0]][location[1]]


def iterate(board) -> Board or None:
    """
    Iterates over the board and splits paths when needed.
    :param board:
    :return: Current board with all work done so far on instance or None if no board exists that can fulfill instance.
    """
    entropy, location, possible_values = board.reduce_entropy()
    if entropy == 0:
        return None
    elif entropy == 1:
        return iterate(board)
    elif entropy == 9:
        return board
    else:
        for attempt in possible_values:
            # print(f"At [{location[0]} {location[1]}] it can possibly be "
            #      f"{[x for x in possible_values]} with current attempt {attempt}")
            new_board = copy.deepcopy(board)
            new_board.board[location[0]][location[1]] = attempt
            new_board = iterate(new_board)
            if isinstance(new_board, Board):
                return new_board
    return None


if __name__ == '__main__':
    raw_board = [  # Deemed the world's hardest sudoku puzzle.
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]
    board_to_be_solved = Board(raw_board, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(iterate(board_to_be_solved))

    # Test with a 4x4 board
    # raw_board = [[2, 0, 0, 0],
    #              [0, 3, 0, 0],
    #              [0, 0, 2, 0],
    #              [1, 0, 0, 3]]
    # board_to_be_solved = Board(raw_board, 4, 4, [1, 2, 3, 3])

    # Tests with  9x9 boards
    # raw_board = [
    #     [0, 0, 4, 0, 5, 0, 0, 0, 0],
    #     [9, 0, 0, 7, 3, 4, 6, 0, 0],
    #     [0, 0, 3, 0, 2, 1, 0, 4, 9],
    #     [0, 3, 5, 0, 9, 0, 4, 8, 0],
    #     [0, 9, 0, 0, 0, 0, 0, 3, 0],
    #     [0, 7, 6, 0, 1, 0, 9, 2, 0],
    #     [3, 1, 0, 9, 7, 0, 2, 0, 0],
    #     [0, 0, 9, 1, 8, 2, 0, 0, 3],
    #     [0, 0, 0, 0, 6, 0, 1, 0, 0]
    # ]
    # raw_board = [
    #     [5, 0, 9, 4, 0, 0, 0, 0, 0],
    #     [0, 0, 3, 0, 0, 0, 6, 9, 0],
    #     [0, 1, 0, 0, 0, 0, 0, 0, 5],
    #     [0, 5, 0, 1, 8, 0, 0, 0, 0],
    #     [3, 0, 0, 0, 5, 0, 0, 0, 7],
    #     [0, 0, 0, 0, 9, 6, 0, 5, 0],
    #     [9, 0, 0, 0, 0, 0, 0, 7, 0],
    #     [0, 3, 8, 0, 0, 0, 5, 0, 0],
    #     [0, 0, 0, 0, 0, 7, 1, 0, 3]
    # ]
    # raw_board = [
    #     [5, 0, 7, 2, 0, 0, 0, 9, 0],
    #     [0, 0, 6, 0, 3, 0, 7, 0, 1],
    #     [4, 0, 0, 0, 0, 0, 0, 6, 0],
    #     [1, 0, 0, 4, 9, 0, 0, 0, 7],
    #     [0, 0, 0, 5, 0, 8, 0, 0, 0],
    #     [8, 0, 0, 0, 2, 7, 0, 0, 5],
    #     [0, 7, 0, 0, 0, 0, 0, 0, 9],
    #     [2, 0, 9, 0, 8, 0, 6, 0, 0],
    #     [0, 4, 0, 0, 0, 9, 3, 0, 8]
    # ]
