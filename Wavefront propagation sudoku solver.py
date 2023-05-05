# -*- coding: utf-8 -*-
"""
Created on Fri May  5 09:38:59 2023

@author: mcgee
"""

import copy
import random
import time

def print_grid(grid):
    #Prints the Sudoku grid in a human-readable format.
    for i in range(len(grid)):
        if i % 2 == 0 and i != 0:
            print("- - - - - - - - - - - - - - - ")
        for j in range(len(grid[0])):
            if j % 2 == 0 and j != 0:
                print(" | ", end="")
            if isinstance(grid[i][j], list):
                print(".", end=" ")
            else:
                print(str(grid[i][j]), end=" ")
        print()

def get_row(grid, row_index):
    #Returns the values in the given row of the grid.
    return [grid[row_index][i] for i in range(len(grid[0]))]

def get_column(grid, col_index):
    #Returns the values in the given column of the grid.
    return [grid[i][col_index] for i in range(len(grid))]

def get_square(grid, row_index, col_index):
    #Returns the values in the square containing the given row and column of the grid.
    square_size = int(len(grid)**0.5)
    row_start = (row_index // square_size) * square_size
    col_start = (col_index // square_size) * square_size
    square = []
    for i in range(row_start, row_start + square_size):
        for j in range(col_start, col_start + square_size):
            square.append(grid[i][j])
    return square

def get_possibilities(grid, row_index, col_index):
    #Returns a list of the possible values for the given empty location in the grid.
    row_values = get_row(grid, row_index)
    col_values = get_column(grid, col_index)
    square_values = get_square(grid, row_index, col_index)
    all_values = list(row_values + col_values + square_values)
    return [i for i in range(1, len(grid)+1) if i not in all_values]

def find_next_empty(grid):
    #Returns the row and column indices of the next empty location in the grid, or None if the grid is full.
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if isinstance(grid[i][j], list):
                return (i, j)
    return None

def solve_sudoku(grid):
    #Solves the Sudoku grid using the wavefront propagation method.
    while True:
        next_empty = find_next_empty(grid)
        if not next_empty:
            return grid
        row_index, col_index = next_empty
        possibilities = get_possibilities(grid, row_index, col_index)
        if len(possibilities) == 0:
            return None
        elif len(possibilities) == 1:
            grid[row_index][col_index] = possibilities[0]
        else:
            grid[row_index][col_index] = possibilities
    return grid

def is_valid(grid):
    #will check whether the given grid is a valid solution to a Sudoku grid.
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if isinstance(grid[i][j], list):
                return False
            row_values = get_row(grid, i)
            col_values = get_column(grid, j)
            square_values = get_square(grid, i, j)
            all_values = set(row_values + col_values + square_values)
            if len(all_values) != len(grid):
                return

def test_solver(grid):
    #returns the time taken in seconds.
    start_time = time.time()
    solution = solve_sudoku(grid)
    end_time = time.time()
    if solution is None:
        print("Unable to solve the Sudoku grid.")
    elif is_valid(solution):
        print("Sudoku grid solved in {:.4f} seconds.".format(end_time - start_time))
        print_grid(solution)
    else:
        print("Solution to the Sudoku grid is invalid.")
    return end_time - start_time


# 4x4 puzzle
grid = [[1, [3], 4, 2],
    [[3, 4], 2, 1, [3]],
    [2, 1, [3], 4],
    [[3], 4, 2, 1]]



   
grid3 = [[[1,2,4], [4, 2], 6, [1, 2, 5], [1, 2, 4, 5], 3],
    [5, [2, 3, 4, 6], [2, 4], [1, 2, 3, 6], [1, 2, 3, 4], [1, 2]],
    [[2, 6], 1, 3, 4, [2, 5], [2, 5]],
    [[1, 2, 3, 4], [2, 3, 4], [2, 4, 5], [1, 2, 3, 5], [1, 2, 3, 4, 5], 6],
    [[2, 3, 4 , 6], [2, 3, 4, 6], 1, [2, 3, 5, 6], [2, 3, 4, 5], []],
    [[1, 2, 3], 5, [1,2], [1, 2, 3], 6, 4]]
print("Original puzzle:")
print_grid(grid)
solved_grid = solve_sudoku(grid)
print("Solved puzzle:")
print_grid(solved_grid)


