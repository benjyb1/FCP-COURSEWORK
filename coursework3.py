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

grids = [(grid1, 2, 2), (grid2, 2, 2), (grid3, 2, 2), (grid4, 2, 2), (grid5, 2, 2),(grid6,2,3), (grid7,3,3)]
'''
===================================
DO NOT CHANGE CODE ABOVE THIS LINE
===================================
'''

import matplotlib.pyplot as plt
import numpy as np
import sys

print(sys.argv)  # Prints the command line arguments as items in a list ['filename.py', 'flag']

flags = ['-explain', '-profile', '-hint', '-hint_explain', '-file']
hint = False
explain = False
hint_explain = False
profile = False
file = False
file_explain = False
'''
For the comment line arguments, variables are set as False by default, and if they are in the
sys.argv, they're reset as True
'''
if '-explain' in sys.argv and not '-hint' in sys.argv:
    explain = True
if '-hint' in sys.argv and not '-explain' in sys.argv:
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

# Global N will be used later, this represents the Number after the Hint flag
if file_explain:
    file_names = []
    for argument in sys.argv:
        if len(argument) == 1:
            global_N = argument
        else:
            global_N = 500000  # arbitrary large constant
            if argument not in flags: #If the arg is longer than 1, it must be a filename
                file_names.append(argument)
                file_names=file_names[1:]

# print('these are filenames', file_names)


def output_grid_to_file(output_file, grid):
    with open(output_file, 'w') as t:
        t.write(str(grid))


def input_file_to_grid(input_file, output_file):
    # open the file for reading
    # inputfile,outputfile=file_names=[1],file_names[2] #The first file_name is coursework3.py
    with open(input_file, 'r') as f:
        # read the file contents as a list of lines
        lines = f.readlines()
        #print('lines=', lines)
        #input_row = len(lines[1])
        #input_col = len(lines)
        #print('input row=', input_row)
        #print('input col=', input_col)
    # create an empty list to hold the grid
    grid = []
    # loop through the lines and split them into individual elements
    for line in lines:
        row = line.strip().split(', ')
        #print(row)
        # convert each element to an integer and append the row to the grid
        grid.append([int(float(x)) for x in row])
        output_grid_to_file(output_file, grid)


    # print the grid to verify the results
    #return grid


def check_section(section, n):
    '''This functoin checks the specified section of the grid to see if its correct.
    Args: Section - Row/Column/Square of the grid
          n= Length of section
    
    '''

    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n + 1)]):
        return True
    return False


def random_solve(grid, n_rows, n_cols, max_tries=50000):
    '''
	This function uses random trial and error to solve a Sudoku grid

	args: grid, n_rows, n_cols, max_tries
	return: A solved grid (as a nested list), or the original grid if no solution is found
	'''

    for i in range(max_tries):
        possible_solution = fill_board_randomly(grid, n_rows, n_cols)
        if check_solution(possible_solution, n_rows, n_cols):
            return possible_solution

    return grid


def fill_board_randomly(grid, n_rows, n_cols):
    '''
	This function will fill an unsolved Sudoku grid with random numbers

	args: grid, n_rows, n_cols
	return: A grid with all empty values filled in
	'''
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
    '''
    This function creates a new list of lists, based on the numbers in the subgrid.
    Returns: the list of lists form the square. 
    '''
    squares = []
    for i in range(n_cols):
        rows = (i*n_rows, (i+1)*n_rows)
        for j in range(n_rows):
            cols = (j*n_cols, (j+1)*n_cols)
            square = []
            for k in range(rows[0], rows[1]):
                line = grid[k][cols[0]:cols[1]]
                square +=line
            squares.append(square)
    return(squares)


def get_subgrid(row, col):
    '''This function outputs the index of the subgrid of any coordinate so that you can use
    it alongside the get_squares function in the form:
        get_squares(variables)[subgrid]
        in order to output the list of numbers in the specific subgrid youre looking at.
    Args: Row - x coordinate 
          Col - y coordinate
    
        '''
    # determine the row and column indices of the subgrid containing the coordinate
    row = row // 2
    col = col // 2
    # calculate the subgrid number based on the row and column indices
    subgrid = row * 2 + col
    return subgrid

def check_line(line,n):
    for value in line:
        if value == n:
            return False 
    return True
def check_square(grid,x,y,value,n_rows,n_cols):
    x = (x // n_rows)*n_rows
    y = (y // n_cols)*n_cols
    for i in range(n_rows):
        for j in range(n_cols):
            if grid[x+i][y+j] == value:
                return False
    return True


# To complete the first assignment, please write the code for the following function
def check_solution(grid, n_rows, n_cols):
    '''
    This function is used to check whether a sudoku board has been correctly solved

    args: grid - representation of a suduko board as a nested list.
    returns: True (correct solution) or False (incorrect solution)
    '''
    n = n_rows * n_cols

    for row in grid:
        if check_section(row, n) == False:
            return False

    for i in range(n_rows ** 2):
        column = []
        for row in grid:
            column.append(row[i])

        if check_section(column, n) == False:
            return False

    squares = get_squares(grid, n_rows, n_cols)
    for square in squares:
        if check_section(square, n) == False:
            return False

    return True


def find_empty(grid,n_rows,n_cols):
    
    '''
    This function returns the index (i, j) to the first zero element in a sudoku grid
    If no such element is found, it returns None

    args: grid
    return: A tuple (i,j) where i and j are both integers, or None
    '''
    empty_space=False
    n=n_rows*n_cols
    for i in range(n):
        for j in range(n):
            if grid[i][j]==0:
                empty_space=(i,j)
    return empty_space

def is_valid_value(grid, n_rows, n_cols, row, col, value,row_coord,col_coord):
    '''This function returns a bool of whether the specified value is in any of the subsections'''
    valid_value = check_line(row,value) and check_line(col,value) and check_square(grid,row_coord,col_coord,value,n_rows,n_cols)
    return valid_value

def recursive_solve(grid, n_rows, n_cols):
    '''
    This function uses recursion to exhaustively search all possible solutions to a grid
    until the solution is found
    args: grid, n_rows, n_cols
    return: A solved grid (as a nested list), or None
    '''
    # Calculate the highest value that can appear in the grid
    max_value = n_rows * n_cols

    # Find the coordinates of an empty cell
    empty_cell = find_empty(grid, n_rows, n_cols)

    if empty_cell:
        # Unpack the coordinates of the empty cell
        row_coord = empty_cell[0]
        col_coord = empty_cell[1]
        row = grid[row_coord]
        col = list(zip(*grid))[col_coord]
        # Try to fill the empty cell with each value from 1 to max_value
        for value in range(1, max_value + 1):
            # Check that the value is not already in the same row, column, or square
            if is_valid_value(grid, n_rows, n_cols, row, col, value,row_coord,col_coord):
                # Fill the empty cell with the value
                grid[row_coord][col_coord] = value

                # Recursively solve the updated grid
                solution = recursive_solve(grid, n_rows, n_cols)

                # If a solution was found, return it
                if solution is not None:
                    return solution

                # If no solution was found, undo the previous change and continue with the next value
                
                grid[row_coord][col_coord] = 0

        # If no valid value was found, backtrack to the previous cell
        return None
    else:
        # If there are no more empty cells, the puzzle is solved
        return grid

def solve(grid, n_rows, n_cols):
    '''
    Solve function for Sudoku coursework.
    Comment out one of the lines below to either use the random or recursive solver
    '''
    # return flag_hint(grid, n_rows, n_cols, global_N)
    # return random_solve(grid, n_rows, n_cols)

    # return fill_board_randomly(grid, n_rows, n_cols)
    return recursive_solve(grid, n_rows, n_cols)


# if file:
    # global_grid = input_file_to_grid('C:/Users/chiar/onedrive/documents/github/FCP-COURSEWORK/med2.txt', 'C:/Users/chiar/onedrive/documents/github/FCP-COURSEWORK/outputfile1.txt')
    # print(global_grid)
    #output_grid = recursive_solve(global_grid)
    #output_grid_to_file('C:/Users/chiar/onedrive/documents/github/FCP-COURSEWORK/outputfile1.txt', global_grid)

def zeros_index(grid):
    '''This function outputs the coordinates of all the zeros in a grid.
    args: grid, the number of rows, number of columns
    returns: a list of the coordinates of all where the 0s in the grid lie
    '''
    zeros_list = []
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            # The enumerate function pairs the entry with an ascending number
            if col == 0:
                zeros_list.append((row_index, col_index))

    return zeros_list



def get_times(solver, grid, n_rows, n_cols):
    '''
    This function outputs the time taken for a specified solver to solve a specified grid
    Args:
        solver - the specific solver, such as recursive_solve
    Returns: The time taken
    '''

    start_time = time.time()
    solution = solver(grid, n_rows, n_cols)
    elapsed_time = time.time() - start_time
    return elapsed_time


def flag_explain(grid, ans):
    '''Function that relates to the -explain flag.
    args: the inital grid, the solved grid
    return: An explanation for what number to replace each 0 with
    '''
    # Output a list of where the 0s are
    zeros_coords = zeros_index(grid)
    explained = []
    # For each zero coordinate find the corresponding number in the ans grid
    for coord in zeros_coords:
        row = coord[0]
        col = coord[1]
        answer = ans[row][col]
        explained.append(f'Put {answer} in location ({row}, {col})')
    return explained


def flag_hint(grid, n_rows, n_cols, N):
    '''Function that puts back a certain number of zeros into the finished grid,
    Returning the somewhat finished grid
    Also if the hint_explain boul gets called then the function will output
    N lines of the explain function
    
    args: grid,n_rows,n_cols
    N (int)= The global N, the number after the hint flag
    returns: The partially filled answer, and if hint_explain is called, then also the 
    partially included explanation
    '''
    N == int(N)
    # getting the coordinates of the zeros
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
    '''
	This the unimproved function uses recursion to exhaustively search all possible solutions to a grid
	until the solution is found
    This function is purely here for the -profile flag

	args: grid, n_rows, n_cols
	return: A solved grid (as a nested list), or None
	'''

    # N is the maximum integer considered in this board
    n = n_rows * n_cols
    # Find an empty place in the grid
    empty = find_empty(grid,n_rows,n_cols)

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

profile=True
def flag_profile(grid, n_rows, n_cols):
    '''
    This function compares the different solvers' performance on different grids
    '''
    times = []
    solvers = [fill_board_randomly, random_solve, old_recursive_solve, recursive_solve]
    for solver in solvers:
        if check_solution(solver(grid, n_rows, n_cols),n_rows, n_cols):
            times.append(get_times(solver, grid, n_rows, n_cols))
        else:
            times.append(5)

    # Defining the colors of the bars based on their values
    colors = ['red' if t >= 5 else 'blue' for t in times]

    # Plotting the times on a logarithmic scale
    x_labels = ['Fill Randomly', 'Random', 'Old Recursive', 'Recursive']
    x_position = [i for i in range(len(x_labels))]
    plt.bar(x_position, times, color=colors)
    plt.xticks(x_position, x_labels)
    plt.ylabel('Time (s)')
    plt.title('Solver Performance, Log scale')
    labels = ['Reached solution' if t and t <= 9 else 'No solution' if t is None else 'Over 9s' for t in times]
    # Setting the y axis to logarithmic
    plt.yscale('log')
    plt.yticks([10 ** i for i in range(int(np.log10(min(times))), int(np.log10(max(times))) + 1)])
    legend_elements = [Patch(facecolor='blue', label='Reached solution'),Patch(facecolor='red', label='No solution')]
    plt.legend(handles=legend_elements)

    plt.show()

    return

def input_output(input_file, output_file):
    '''Function that relates to the -file flag
        args: the input file, the output file
        Reads the unsolved suduko from the input file, solves it using the recursive solver function, writes the solved grid into the output file
        '''
    # input file,output file = file_names[1],file_names[2] (The first file_name is coursework3.py)
    # open the file for reading
    with open(input_file, 'r') as f:
        # read the file contents as a list of lines
        lines = f.readlines()
        first_line = lines[0].split(',')

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

    #  The recursively solved input grid is named 'output_grid'
    output_grid = recursive_solve(input_grid, input_n_rows, input_n_cols)
    #  Write output grid in output file
    with open(output_file, 'w') as t:
        t.write(str(output_grid))


# if file:
#     input_output('C:/Users/chiar/onedrive/documents/github/FCP-COURSEWORK/grid1.txt',
#              'C:/Users/chiar/onedrive/documents/github/FCP-COURSEWORK/outputfile1.txt')



# If the -explain flag is triggered, output the instructions for each grid
if explain:
    for i in range(len(grids)):
        print('For grid[{}]: {}'.format(i + 1, flag_explain(grids[i][0],
                                                            recursive_solve(grids[i][0], grids[i][1], grids[i][2]))))
if profile:
    print(flag_profile(grid5, 2, 2), 'Profile is working')


def main():
    points = 0
    print("Running test script for coursework 1")
    print("====================================")

    for (i, (grid, n_rows, n_cols)) in enumerate(grids):
        print("Solving grid: %d" % (i + 1))
        start_time = time.time()
        solution = solve(grid, n_rows, n_cols)
        elapsed_time = time.time() - start_time
        print("Solved in: %f seconds" % elapsed_time)

        if hint or hint_explain:
            print(flag_hint(grid, n_rows, n_cols, 2))
        else:
            print(solution)
        if check_solution(solution, n_rows, n_cols):
            print("grid %d correct" % (i + 1))
            points = points + 10

        else:
            print("grid %d incorrect" % (i + 1))

    print("====================================")
    print("Test script complete, Total points: %d" % points)


if __name__ == "__main__":
    main()
output_file = 'output.txt'

# output = main()
# print(output)
# if file:
#     with open(output_file, 'w') as f:
#         mainman=[]
#         mainman.append(main())
#         for line in mainman:
#             print(line,'HELLO')
#             f.write(line)
