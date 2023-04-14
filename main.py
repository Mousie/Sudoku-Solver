"""
File: WaveFunctionCollapse - Sudoku
Author: Christopher Kihano
Date: July 12 2022
Date Updated: August 17 2022

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

            Default setup solves for what is termed "the hardest sukodu"

             Updated to only attempt propagation if there's a solution in the cell.

Further Improvements:
            Looking at other solvers after completing my own, I see what looks to be simpler implementations. However,
            these also seem to use a more brute force method in which all possible values are tried in a cell until a
            no solution cell is found and then backtracking is performed. Should I return to this, I may look more into
            how they solved this problem further, but I'm happy with my solution. They also assume 9x9 boards.
"""

import copy
import math
import time
from dataclasses import dataclass


class Board:
    def __init__(self, board: list[list[int]], possible_values: list):
        """ Board class for passing around board instances and printing and solving boards.
        :param board: A 2D array of the board. 0 denotes unsolved, a list is possible values, others are given values.
        :param possible_values: List of possible values each cell can take on. This includes numbers, letters, objects.
        """
        self.width = len(board)
        self.height = len(board[0])
        self.num_of_cells = self.width * self.height
        self.queue = list()
        self.unsolved = self.width * self.height
        self.board = list()
        self.sub_block = int(math.sqrt(self.width))
        self.possible_values = possible_values.copy()
        self.num_of_possible = len(self.possible_values)
        for y in range(self.height):
            self.board.append(list())
            for x in range(self.width):
                if 0 == board[y][x]:
                    possibilities = possible_values.copy()
                    entropy = 9
                else:
                    possibilities = [board[y][x]]
                    entropy = 1
                    self.queue.append([y, x])
                top_left_x = (x // self.sub_block) * self.sub_block  # Top left x of sub-squares
                top_left_y = (y // self.sub_block) * self.sub_block  # Same but y
                self.board[y].append(Cell(possibilities, entropy, top_left_x, top_left_y))
        self.return_line_string = " ".join(["{" + str(i) + ":3}" for i in range(self.width)]) + '\n'

    def __str__(self):
        return_string = ""
        for row in self.board:
            return_string += self.return_line_string.format(*[str(item.value_used) for item in row])
        return return_string

    def remove_possibility(self, y, x, value):
        cell = self.board[y][x]
        cell.possibilities.remove(value)
        cell.entropy -=1
        if 1 == cell.entropy:
            self.queue.append([y,x])
    def propagate(self, x, y):
        """When there's only one value it can be, reduce entropy of surrounding cells"""
        cell = self.board[y][x]
        value = cell.value_used
        # Remove values from columns and rows
        for i in range(self.width):
            if value in self.board[y][i].possibilities:
                self.remove_possibility(y, i, value)
            if value in self.board[i][x].possibilities:
                self.remove_possibility(i, x, value)
        # Remove values from sub-squares
        for box_y in range(cell.top_left_y, cell.top_left_y + self.sub_block):  # Scan sub-square to find solved cells
            for box_x in range(cell.top_left_x, cell.top_left_x + self.sub_block):
                if value in self.board[box_y][box_x].possibilities:
                    self.remove_possibility(box_y, box_x, value)
        return

    def lowest_entropy(self) -> [int, int]:
        lowest = self.num_of_possible
        lowest_loc = [0, 0]
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell.entropy < lowest and 0 == cell.value_used:
                    lowest = cell.entropy
                    lowest_loc = [y, x]
        return lowest_loc


@dataclass
class Cell:
    possibilities: list[int]
    entropy: int
    top_left_x: int
    top_left_y: int
    value_used: int = 0


def iterate(board: Board):
    for y, x in board.queue:
        cell = board.board[y][x]
        if 0 == cell.value_used:
            if 0 == cell.entropy:
                return None
            elif 1 == cell.entropy:
                cell.value_used = cell.possibilities[0]
                board.propagate(x, y)
                board.unsolved -= 1
                if 0 == board.unsolved:
                    return board
    y, x = board.lowest_entropy()
    board.queue = [[y, x]]
    cell = board.board[y][x]
    for branch in cell.possibilities:
        new_board = copy.deepcopy(board)
        branch_cell = new_board.board[y][x]
        branch_cell.possibilities = [branch]
        branch_cell.entropy = 1
        new_board = iterate(new_board)
        if isinstance(new_board, Board):
            return new_board
    return None


if __name__ == '__main__':
    test_board1 = [  # Deemed the world's hardest sudoku puzzle.
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
    test_board2 = [
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
        [4, 0, 9, 0, 0, 6, 8, 7, 0],
        [0, 0, 0, 9, 0, 0, 1, 0, 0],
        [5, 0, 4, 0, 2, 0, 0, 0, 9],
        [0, 7, 0, 8, 0, 4, 0, 6, 0],
        [6, 0, 0, 0, 3, 0, 5, 0, 2],
        [0, 0, 1, 0, 0, 7, 0, 0, 0],
        [0, 4, 3, 2, 0, 0, 6, 0, 5],
        [0, 0, 0, 0, 0, 5, 0, 0, 0]
    ]
    test_board3 = [
        [0, 0, 4, 0, 5, 0, 0, 0, 0],
        [9, 0, 0, 7, 3, 4, 6, 0, 0],
        [0, 0, 3, 0, 2, 1, 0, 4, 9],
        [0, 3, 5, 0, 9, 0, 4, 8, 0],
        [0, 9, 0, 0, 0, 0, 0, 3, 0],
        [0, 7, 6, 0, 1, 0, 9, 2, 0],
        [3, 1, 0, 9, 7, 0, 2, 0, 0],
        [0, 0, 9, 1, 8, 2, 0, 0, 3],
        [0, 0, 0, 0, 6, 0, 1, 0, 0]
    ]
    test_board4 = [
        [5, 0, 9, 4, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 6, 9, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 5],
        [0, 5, 0, 1, 8, 0, 0, 0, 0],
        [3, 0, 0, 0, 5, 0, 0, 0, 7],
        [0, 0, 0, 0, 9, 6, 0, 5, 0],
        [9, 0, 0, 0, 0, 0, 0, 7, 0],
        [0, 3, 8, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 7, 1, 0, 3]
    ]
    test_board5 = [
        [5, 0, 7, 2, 0, 0, 0, 9, 0],
        [0, 0, 6, 0, 3, 0, 7, 0, 1],
        [4, 0, 0, 0, 0, 0, 0, 6, 0],
        [1, 0, 0, 4, 9, 0, 0, 0, 7],
        [0, 0, 0, 5, 0, 8, 0, 0, 0],
        [8, 0, 0, 0, 2, 7, 0, 0, 5],
        [0, 7, 0, 0, 0, 0, 0, 0, 9],
        [2, 0, 9, 0, 8, 0, 6, 0, 0],
        [0, 4, 0, 0, 0, 9, 3, 0, 8]
    ]
    test_board6 = [[2, 0, 0, 0],
                   [0, 3, 0, 0],
                   [1, 0, 4, 0],
                   [0, 0, 0, 1]]
    board_to_be_solved = Board(test_board1, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    start_time = time.process_time_ns()
    print(iterate(board_to_be_solved))
    end_time = time.process_time_ns()
    print((end_time - start_time) / 10e9)
