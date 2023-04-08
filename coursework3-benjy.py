import random
import copy
import time

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

grids = [(grid1, 2, 2), (grid2, 2, 2), (grid3, 2, 2), (grid4, 2, 2), (grid5, 2, 2)]
'''
===================================
DO NOT CHANGE CODE ABOVE THIS LINE
===================================
'''
import sys
print(sys.argv)  # Prints the command line arguments as items in a list ['filename.py', 'flag']
explain=False
for i in sys.argv:
    if i == '-explain':
        explain=True


if len(sys.argv) == 3:# Check there are three command line arguments (the filename and either 'hint' 'number' or 'INPUT' 'OUTPUT')
    flag = sys.argv[1]  # Assign the second command line argument to 'flag'
    number = sys.argv[2]  # Assign the third command line argument to 'number'
    print(number)  # Printing the number entered after 'hint' by the user in terminal
    number = int(number)  # Changing the number's type from string to integer
    #print(type(number))
    print(flag)  # Printing the flag entered by the user in terminal


def check_section(section, n):
    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n + 1)]):
        return True
    return False


def get_squares(grid, n_rows, n_cols):
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

'''This function outputs the index of the subgrid of any coordinate so that you can use
it alongside the get_squares function in the form:
    get_squares(variables)[subgrid]
    in order to output the list of numbers in the specific subgrid youre looking at'''
    
def get_subgrid(row,col):
    # determine the row and column indices of the subgrid containing the coordinate
    row = row // 2
    col = col // 2
    # calculate the subgrid number based on the row and column indices
    subgrid = row * 2 + col
    return subgrid


# Defining a function that outputs the list of possible values left for any coordinate
'''BTW ive renamed this from elimnates_values to possible_values for clarity'''
def possible_values(grid, row, col, n, n_rows, n_cols):
    # Find values already present in the sudoku, create empty list p_values
    p_values = []
    row_values = grid[row]
    col_values = [grid[i][col] for i in range(n)]
    #Find the subgrid values
    subgrid=get_subgrid(row,col)
    square_values = get_squares(grid, n_rows, n_cols)[subgrid]
    # All values 1 to n+1 are possible before we check the rows, columns and squares
    possible_values=[]
    possible_values.append([i for i in range(1,n+1)])
    # Put all values present into a single list
    values_present = row_values + col_values + square_values
    # Also put all possible values 1 to n+1 into the list
    possible_values.append(values_present)
    # The extend values just takes a list of nested lists and returns a normal list
    final_values=[]
    for sublist in possible_values:
        final_values.extend(sublist)
    # if the number is in the list more than once, remove it from the list
    for element in final_values:
        if final_values.count(element) ==1:
            p_values.append(element)
    return p_values


'''This function will return the coordinates of the positions with the lowest amount of possibilites
It outputs a list in the form of: [possible value(s)],coordiantes(x,y)
'''

def find_lowest_possibilites(grid,n,n_rows,n_cols):
    possible_list=[]
    for i in range(len(zeros_index(grid))):
        row=zeros_index(grid)[i][0]
        col=zeros_index(grid)[i][1]
        # Finding the coordinates of the 0's
        possible_list.append((possible_values(grid,row,col,n,n_rows,n_cols),row,col))
        # Adding to the list the possible values, and the row and column theryre in
    possible_list=sorted(possible_list)
    
    return possible_list

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

def find_empty(grid):
    '''
    This function returns the index (i, j) to the first zero element in a sudoku grid
    If no such element is found, it returns None

    args: grid
    return: A tuple (i,j) where i and j are both integers, or None
    '''

    for i in range(len(grid)):
        row = grid[i]
        for j in range(len(row)):
            if grid[i][j] == 0:
                return (i, j)

    return None

def recursive_solve(grid, n_rows, n_cols):
    '''
    This function uses recursion to exhaustively search all possible solutions to a grid
    until the solution is found

    args: grid, n_rows, n_cols
    return: A solved grid (as a nested list), or None
    '''
    # Using the current_grid variable so the original grids aren't changed
    # The copy.deepcopy allows for nested lists to be fully copied.
    current_grid=copy.deepcopy(grid)
    # N is the maximum integer considered in this board
    
    n = n_rows * n_cols
    # Find an empty place in the grid
    empty = find_empty(current_grid)
    # If there's no empty places left, check if we've found a solution
    if not empty:
        # If the solution is correct, return it.
        if check_solution(current_grid, n_rows, n_cols):
            return current_grid
        else:
            # If the solution is incorrect, return None
            return None
    else:
        row, col = empty
        p_values=possible_values(current_grid, row, col, n, n_rows, n_cols)
        
        # Going through only the possible values
        for value in p_values:

            # Place the value into the grid
            current_grid[row][col] = value
            # Recursively solve the grid
            ans = recursive_solve(current_grid, n_rows, n_cols)
            # If we've found a solution, return it
            if ans:
                return ans 

            # If we couldn't find a solution, that must mean this value is incorrect.
            # Reset the grid for the next iteration of the loop
            current_grid[row][col] = 0 
        # If we get here, we've tried all possible values. Return none to indicate the previous value is incorrect.
        return None


def solve(grid, n_rows, n_cols):
    '''
    Solve function for Sudoku coursework.
    Comment out one of the lines below to either use the random or recursive solver
    '''

    # return random_solve(grid, n_rows, n_cols)
    return recursive_solve(grid, n_rows, n_cols)


def zeros_index(grid):
    '''This function outputs the coordinates of all the zeros in a grid.
    args: grid, the number of rows, number of columns
    returns: a list of the coordinates of all where the 0s in the grid lie
    '''
    zeros_list=[]
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            # The enumerate function pairs the entry with an ascending number
            if col == 0:
                zeros_list.append((row_index, col_index))
     
    return zeros_list


def flag_explain(grid,ans):
    '''Function that relates to the -explain flag.
    args: the inital grid, the solved grid
    return: An explanation for what number to replace each 0 with
    '''
    # Output a list of where the 0s are
    zeros_coords=zeros_index(grid)
    explained=[]
    # For each zero coordinate find the corresponding number in the ans grid
    for coord in zeros_coords:
        row=coord[0]
        col=coord[1]
        answer=ans[row][col]
        explained.append(f'Put {answer} in location ({row}, {col})')
    return explained

# If the -explain flag is triggered, output the instructions for each grid
if explain:
    for i in range(len(grids)):
        print('For grid[{}]: {}'.format(i+1, flag_explain(grids[i][0], recursive_solve(grids[i][0], grids[i][1], grids[i][2]))))

'''
===================================
DO NOT CHANGE CODE BELOW THIS LINE
===================================
'''



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