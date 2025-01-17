import random
import copy
import time
import matplotlib as plt
from matplotlib.patches import Patch

# Grids 1-4 are 2x2
grid1 = [
    [1, 0, 4, 2],
    [4, 2, 1, 3],
    [2, 1, 3, 4],
    [3, 4, 2, 1]]

grid2 = [
    [1, 0, 4, 2],
    [4, 2, 1, 3],
    [2, 1, 0, 4],
    [3, 4, 2, 1]]

grid3 = [
    [1, 0, 4, 2],
    [4, 2, 1, 0],
    [2, 1, 0, 4],
    [0, 4, 2, 1]]

grid4 = [
    [1, 0, 4, 2],
    [0, 2, 1, 0],
    [2, 1, 0, 4],
    [0, 4, 2, 1]]

grid5 = [
    [1, 0, 0, 2],
    [0, 0, 1, 0],
    [0, 1, 0, 4],
    [0, 0, 0, 1]]

grid6 = [

    [0, 0, 6, 0, 0, 3],
    [5, 0, 0, 0, 0, 0],
    [0, 1, 3, 4, 0, 0],
    [0, 0, 0, 0, 0, 6],
    [0, 0, 1, 0, 0, 0],
    [0, 5, 0, 0, 6, 4]]

grid7 = [[0, 2, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 6, 0, 4, 0, 0, 0, 0],
         [5, 8, 0, 0, 9, 0, 0, 0, 3],
         [0, 0, 0, 0, 0, 3, 0, 0, 4],
         [4, 1, 0, 0, 8, 0, 6, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 9, 5],
         [2, 0, 0, 0, 1, 0, 0, 8, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 3, 1, 0, 0, 8, 0, 5, 7]]

grids = [(grid1, 2, 2), (grid2, 2, 2), (grid3, 2, 2), (grid4, 2, 2), (grid5, 2, 2), (grid6, 2, 3), (grid7, 3, 3)]
'''
===================================
DO NOT CHANGE CODE ABOVE THIS LINE
===================================
'''

import matplotlib.pyplot as plt
import numpy as np
import sys

flags = ['-explain', '-profile', '-hint', '-file']
hint = False
explain = False
hint_explain = False
profile = False
file = False
file_explain = False

"""
For the command line arguments, variables are set as False by default, and if they are in the
sys.argv, they're reset as True
"""

for argument in sys.argv:
    if len(argument) == 1:
        global_N = int(argument)
    else:
        global_N = 500000  # Arbitrary large constant

if '-explain' in sys.argv and '-hint' not in sys.argv:
    explain = True
if '-hint' in sys.argv and '-explain' not in sys.argv:
    hint = True
if '-explain' in sys.argv and '-hint' in sys.argv:
    hint_explain = True
if '-profile' in sys.argv:  # The profile flag overrides all other flags as they make the code take longer
    profile = True
    hint = False
    explain = False
    hint_explain = False
if '-file' in sys.argv:
    file = True
if '-file' in sys.argv and '-explain' in sys.argv:
    file_explain = True


def check_section(section, n):
    """
    This function checks the specified section of the grid to see if it's correct.
    Args: Section - Row/Column/Square of the grid
          n = Length of section
    """

    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n + 1)]):
        return True
    return False


def random_solve(grid, n_rows, n_cols, max_tries=50000):
    """
	This function uses random trial and error to solve a Sudoku grid
	Args: grid, n_rows, n_cols, max_tries
	Return: A solved grid (as a nested list), or the original grid if no solution is found
	"""

    for i in range(max_tries):
        possible_solution = fill_board_randomly(grid, n_rows, n_cols)
        if check_solution(possible_solution, n_rows, n_cols):
            return possible_solution

    return grid


def fill_board_randomly(grid, n_rows, n_cols):
    """
	This function will fill an unsolved Sudoku grid with random numbers
	Args: grid, n_rows, n_cols
	Return: A grid with all empty values filled in
	"""

    n = n_rows * n_cols
    # Make a copy of the original grid
    filled_grid = copy.deepcopy(grid)

    # Loop through the rows
    for i in range(len(grid)):
        # Loop through the columns
        for j in range(len(grid[0])):
            # If we find a zero, fill it in with a random integer
            if grid[i][j] == 0:
                filled_grid[i][j] = random.randint(1, n)

    return filled_grid


def get_squares(grid, n_rows, n_cols):
    """
    This function creates a new list of lists, based on the numbers in the subgrid.
    Returns: the list of lists form the square.
    """
    squares = []
    for i in range(n_cols):
        rows = (i * n_rows, (i + 1) * n_rows)
        for j in range(n_rows):
            cols = (j * n_cols, (j + 1) * n_cols)
            square = []
            for k in range(rows[0], rows[1]):
                line = grid[k][cols[0]:cols[1]]
                square += line
            squares.append(square)
    return squares


def get_subgrid(row, col):
    """
    This function outputs the index of the subgrid of any coordinate so that you can use
    it alongside the get_squares function in the form:
        get_squares(variables)[subgrid]
        in order to output the list of numbers in the specific subgrid you're looking at.
    Args: Row - x coordinate
          Col - y coordinate
    """
    # Determine the row and column indices of the subgrid containing the coordinate
    row = row // 2
    col = col // 2
    # Calculate the subgrid number based on the row and column indices
    subgrid = row * 2 + col
    return subgrid


def check_line(line, n):
    for value in line:
        if value == n:
            return False
    return True


def check_square(grid, x, y, value, n_rows, n_cols):
    x = (x // n_rows) * n_rows
    y = (y // n_cols) * n_cols
    for i in range(n_rows):
        for j in range(n_cols):
            if grid[x + i][y + j] == value:
                return False
    return True


def check_solution(grid, n_rows, n_cols):
    """
    This function is used to check whether a sudoku board has been correctly solved
    Args: grid - representation of a sudoku board as a nested list.
    Returns: True (correct solution) or False (incorrect solution)
    """
    n = n_rows * n_cols

    for row in grid:
        if not check_section(row, n):
            return False

    for i in range(n_rows ** 2):
        column = []
        for row in grid:
            column.append(row[i])

        if not check_section(column, n):
            return False

    squares = get_squares(grid, n_rows, n_cols)
    for square in squares:
        if not check_section(square, n):
            return False

    return True


def find_empty(grid, n_rows, n_cols):
    """
    This function returns the index (i, j) to the first zero element in a sudoku grid
    If no such element is found, it returns None
    Args: grid
    Return: A tuple (i,j) where i and j are both integers, or None
    """
    empty_space = False
    n = n_rows * n_cols
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                empty_space = (i, j)
    return empty_space


def is_valid_value(grid, n_rows, n_cols, row, col, value, row_coord, col_coord):
    """
    This function returns a bool of whether the specified value is in any of the subsections
    """
    valid_value = check_line(row, value) and check_line(col, value) and check_square(grid, row_coord, col_coord, value,
                                                                                     n_rows, n_cols)
    return valid_value


def recursive_solve(grid, n_rows, n_cols):
    """
    This function uses recursion to exhaustively search all possible solutions to a grid
    until the solution is found
    Args: grid, n_rows, n_cols
    Return: A solved grid (as a nested list), or None
    """
    current_grid = copy.deepcopy(grid)
    # Calculate the highest value that can appear in the grid
    max_value = n_rows * n_cols

    # Find the coordinates of an empty cell
    empty_cell = find_empty(current_grid, n_rows, n_cols)

    if empty_cell:
        # Unpack the coordinates of the empty cell
        row_coord = empty_cell[0]
        col_coord = empty_cell[1]
        row = current_grid[row_coord]
        col = list(zip(*current_grid))[col_coord]
        # Try to fill the empty cell with each value from 1 to max_value
        for value in range(1, max_value + 1):
            # Check that the value is not already in the same row, column, or square
            if is_valid_value(current_grid, n_rows, n_cols, row, col, value, row_coord, col_coord):
                # Fill the empty cell with the value
                current_grid[row_coord][col_coord] = value

                # Recursively solve the updated grid
                solution = recursive_solve(current_grid, n_rows, n_cols)

                # If a solution was found, return it
                if solution is not None:
                    return solution

                # If no solution was found, undo the previous change and continue with the next value

                current_grid[row_coord][col_coord] = 0

        # If no valid value was found, backtrack to the previous cell
        return None
    else:
        # If there are no more empty cells, the puzzle is solved
        return current_grid


def solve(grid, n_rows, n_cols):
    """
    Solve function for Sudoku coursework.
    Comment out one of the lines below to either use the random or recursive solver
    """
    # return flag_hint(grid, n_rows, n_cols, global_N)
    # return random_solve(grid, n_rows, n_cols)

    # return fill_board_randomly(grid, n_rows, n_cols)
    return recursive_solve(grid, n_rows, n_cols)


def zeros_index(grid):
    """
    This function outputs the coordinates of all the zeros in a grid.
    Args: grid, the number of rows, number of columns
    Returns: a list of the coordinates of all where the 0s in the grid lie
    """
    zeros_list = []
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            # The enumerate function pairs the entry with an ascending number
            if col == 0:
                zeros_list.append((row_index, col_index))
    return zeros_list


def get_times(solver, grid, n_rows, n_cols):
    """
    This function outputs the time taken for a specified solver to solve a specified grid
    Args: solver - the specific solver, such as recursive_solve
    Returns: The time taken
    """
    start_time = time.time()
    solution = solver(grid, n_rows, n_cols)
    elapsed_time = time.time() - start_time
    print(solution)
    return elapsed_time



def flag_explain(grid, ans):
    """
    Function that relates to the -explain flag.
    Args: the initial grid, the solved grid
    Return: An explanation for what number to replace each 0 with
    """
    # Output a list of where the 0s are
    zeros_coords = zeros_index(grid)
    explanation = []
    # For each zero coordinate find the corresponding number in the ans grid
    for coord in zeros_coords:
        row = coord[0]
        col = coord[1]
        answer = ans[row][col]
        explanation.append(f'Put {answer} in location ({row}, {col})')
    return explanation


def flag_hint(grid, n_rows, n_cols, N):
    """
    Function that puts back a certain number of zeros into the finished grid,
    Returning the somewhat finished grid.
    Also, if the hint_explain bool gets called then the function will output
    N lines of the explain function

    Args: grid, n_rows, n_cols
    N (int)= The global N, the number after the hint flag
    Returns: The partially filled answer, and if hint_explain is called, then also the
    partially included explanation
    """
    # Getting the coordinates of the zeros
    zeros = zeros_index(grid)
    # Only keeping N elements from the list
    del zeros[:N]
    # Getting the solved grid
    answer = recursive_solve(grid, n_rows, n_cols)
    for coord in zeros:
        # Replacing N solved numbers from the end with 0
        row = coord[0]
        col = coord[1]
        answer[row][col] = 0
    # Outputting N explanation lines
    if hint_explain:
        explained = flag_explain(grid, answer)
        for i in range(N):
            explained_list = explained[:N]
        # if no hint_explain, just return normal partially filled grid
        return answer, explained_list
    return answer


def old_recursive_solve(grid, n_rows, n_cols):
    """
	This the unimproved function uses recursion to exhaustively search all possible solutions to a grid
	until the solution is found
    This function is purely here for the -profile flag

	Args: grid, n_rows, n_cols
	Return: A solved grid (as a nested list), or None
	"""

    # N is the maximum integer considered in this board
    n = n_rows * n_cols
    # Find an empty place in the grid
    empty = find_empty(grid, n_rows, n_cols)

    # If there's no empty places left, check if we've found a solution
    if not empty:
        # If the solution is correct, return it.
        if check_solution(grid, n_rows, n_cols):
            return grid
        else:
            # If the solution is incorrect, return None
            return None
    else:
        row, col = empty

    # Loop through possible values
    for i in range(1, n + 1):

        # Place the value into the grid
        grid[row][col] = i
        # Recursively solve the grid
        ans = old_recursive_solve(grid, n_rows, n_cols)

        # If we've found a solution, return it
        if ans:
            return ans

        # If we couldn't find a solution, that must mean this value is incorrect.
        # Reset the grid for the next iteration of the loop
        grid[row][col] = 0

    # If we get here, we've tried all possible values. Return none to indicate the previous value is incorrect.
    return None


def flag_profile(grid, n_rows, n_cols):
    """
    This function compares the different solvers' performance on different grids
    Returns: A plot for each grid the different solvers have solved
    It will return a red bar and give it a arbitrary large time if the solver didn't reach an answer
    It will return a Blue bar if the solver was succesful, with the times being on a logarithmic scale as the times are often
    magnitudes different.
    """
    times = []
    solvers = [fill_board_randomly, random_solve, recursive_solve]
    for solver in solvers:
        if check_solution(solver(grid, n_rows, n_cols), n_rows, n_cols):
            times.append(get_times(solver, grid, n_rows, n_cols))
        else:
            times.append(5)

    # Defining the colors of the bars based on their values
    colors = ['red' if t >= 5 else 'blue' for t in times]

    # Plotting the times on a logarithmic scale
    x_labels = ['Fill Randomly', 'Random', 'Recursive']
    x_position = [i for i in range(len(x_labels))]
    plt.bar(x_position, times, color=colors)
    plt.xticks(x_position, x_labels)
    plt.ylabel('Time (s) Log scale')
    plt.title('Solver Performance')
    # Setting the y-axis to logarithmic
    plt.yscale('log')
    plt.yticks([10 ** i for i in range(int(np.log10(min(times))), int(np.log10(max(times))) + 1)])
    legend_elements = [Patch(facecolor='blue', label='Reached solution'), Patch(facecolor='red', label='No solution')]
    plt.legend(handles=legend_elements)

    plt.show()

    return


def flag_input_to_grid(input_file):
    """
    Function that takes the input file and outputs the parsed input grid
    Returns: 
        The parsed input grid taken from the input file
        The input grid's row and column length
    """
    with open(input_file, 'r') as f:
        # Read the file contents as a list of lines
        lines = f.readlines()
        first_line = lines[0].split(',')
        #  Finding n_rows and n_cols, based off the size of the inputted grid
        if len(first_line) == 4:
            input_n_rows = 2
            input_n_cols = 2
        if len(first_line) == 9:
            input_n_rows = 3
            input_n_cols = 3
        if len(first_line) == 6:
            input_n_rows = 2
            input_n_cols = 3

    # Create an empty list to hold the grid called 'input_grid'
    input_grid = []
    # Loop through the lines and split them into individual elements
    for line in lines:
        row = line.strip().split(', ')

        # Convert each element to an integer and append the row to the grid
        input_grid.append([int(float(x)) for x in row])
    return input_grid, input_n_rows, input_n_cols


def flag_input_output(input_file, output_file):
    """
    Function that uses the flag_input_to_grid function as an input and outputs the solved grid
    Takes the input grid and prints the output grid with the specified flags
    Returns:
        Writes into a specified file the solved grid, along with the outputs from specified flags.
    """
    input_grid, n_rows, n_cols = flag_input_to_grid(input_file)
    output_grid = recursive_solve(input_grid, n_rows, n_cols)
    #  Write output grid in output file
    with open(output_file, 'w') as t:
        if hint or hint_explain:
            t.write(str(flag_hint(input_grid, n_rows, n_cols, global_N)))
        else:
            t.write(str(output_grid))
            if explain:
                t.write(str(flag_explain(input_grid, output_grid)))


# Getting the file names from the command line
if file or file_explain:
    # Create an empty list to append the filenames to
    file_names = []
    for argument in sys.argv:
        if len(argument) != 1:
            if argument not in flags:  # If the arg is longer than 1, it must be a filename
                file_names.append(argument)
    the_file_names = file_names[1:]
if file:
    flag_input_output(the_file_names[0], the_file_names[1])
    global_file_grid = flag_input_to_grid(the_file_names[0])


'''
WAVEFRONT PROPOGATION
The next section is Task 3, the wavefront propogation.
It works less efficiently than the improved recursive solver, so the main function will remain using the recursive solver
'''
def print_grid_wavefront(grid):
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

def get_row_wavefront(grid, row_index):
    #Returns the values in the given row of the grid.
    return [grid[row_index][i] for i in range(len(grid[0]))]

def get_column_wavefront(grid, col_index):
    #Returns the values in the given column of the grid.
    return [grid[i][col_index] for i in range(len(grid))]

def get_square_wavefront(grid, row_index, col_index):
    #Returns the values in the square containing the given row and column of the grid.
    square_size = int(len(grid)**0.5)
    row_start = (row_index // square_size) * square_size
    col_start = (col_index // square_size) * square_size
    square = []
    for i in range(row_start, row_start + square_size):
        for j in range(col_start, col_start + square_size):
            square.append(grid[i][j])
    return square

def get_possibilities_wavefront(grid, row_index, col_index):
    #Returns a list of the possible values for the given empty location in the grid.
    row_values = get_row_wavefront(grid, row_index)
    col_values = get_column_wavefront(grid, col_index)
    square_values = get_square_wavefront(grid, row_index, col_index)
    all_values = list(row_values + col_values + square_values)
    return [i for i in range(1, len(grid)+1) if i not in all_values]

def find_next_empty_wavefront(grid):
    #Returns the row and column indices of the next empty location in the grid, or None if the grid is full.
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if isinstance(grid[i][j], list):
                return (i, j)
    return None

def solve_sudoku_wavefront(grid):
    #Solves the Sudoku grid using the wavefront propagation method.
    while True:
        next_empty = find_next_empty_wavefront(grid)
        if not next_empty:
            return grid
        row_index, col_index = next_empty
        possibilities = get_possibilities_wavefront(grid, row_index, col_index)
        if len(possibilities) == 0:
            return None
        elif len(possibilities) == 1:
            grid[row_index][col_index] = possibilities[0]
        else:
            grid[row_index][col_index] = possibilities
    return grid

def is_valid_wavefront(grid):
    #will check whether the given grid is a valid solution to a Sudoku grid.
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if isinstance(grid[i][j], list):
                return False
            row_values = get_row_wavefront(grid, i)
            col_values = get_column_wavefront(grid, j)
            square_values = get_square_wavefront(grid, i, j)
            all_values = set(row_values + col_values + square_values)
            if len(all_values) != len(grid):
                return

def test_solver(grid):
    #returns the time taken in seconds.
    start_time = time.time()
    solution = solve_sudoku_wavefront(grid)
    end_time = time.time()
    if solution is None:
        print("Unable to solve the Sudoku grid.")
    elif is_valid_wavefront(solution):
        print("Sudoku grid solved in {:.4f} seconds.".format(end_time - start_time))
        print_grid_wavefront(solution)
    else:
        print("Solution to the Sudoku grid is invalid.")
    return end_time - start_time
grid = [[1, [3], 4, 2],
    [[3, 4], 2, 1, [3]],
    [2, 1, [3], 4],
    [[3], 4, 2, 1]]


print("Original puzzle:")
print_grid_wavefront(grid)
solved_grid = solve_sudoku_wavefront(grid)
print("Solved puzzle:")
print_grid_wavefront(solved_grid)



'''
END OF TASK 3 WAVEFRONT PROPOGATION
'''

def main():
    points = 0
    print("Running test script for coursework 3")
    print("====================================")

    if file:
        grid, n_rows, n_cols = global_file_grid
        print('Solving Inputted Grid')
        start_time = time.time()
        solution = solve(grid, n_rows, n_cols)
        elapsed_time = time.time() - start_time
        print("Solved in: %f seconds" % elapsed_time)
        if hint or hint_explain:
            print(flag_hint(grid, n_rows, n_cols, global_N))
        elif explain:
            print(flag_explain(grid, solution))
        else:
            print(solution)
        if check_solution(solution, n_rows, n_cols):
            print('Grid Correct')
            points = points + 10
        else:
            print('Grid incorrect')
        if profile:
            flag_profile(grid, n_rows, n_cols)

    else:
        for (i, (grid, n_rows, n_cols)) in enumerate(grids):
            print("Solving grid: %d" % (i + 1))
            start_time = time.time()
            solution = solve(grid, n_rows, n_cols)
            elapsed_time = time.time() - start_time
            print("Solved in: %f seconds" % elapsed_time)
            if hint or hint_explain:
                print(flag_hint(grid, n_rows, n_cols, global_N))
            elif explain:
                print('For grid[{}]: {}'.format(i + 1, flag_explain(grids[i][0],
                                                                    recursive_solve(grids[i][0], grids[i][1],
                                                                                    grids[i][2]))))
            else:
                print(solution)
            if profile:
                flag_profile(grid, n_rows, n_cols)
            if check_solution(solution, n_rows, n_cols):
                print("grid %d correct" % (i + 1))
                points = points + 10

            else:
                print("grid %d incorrect" % (i + 1))
    print("====================================")
    print("Test script complete, Total points: %d" % points)


if __name__ == "__main__":
    main()
