import random
import copy
import time
import matplotlib as plt
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

grid7=[[0, 2, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 6, 0, 4, 0, 0, 0, 0],
[5, 8, 0, 0, 9, 0, 0, 0, 3],
[0, 0, 0, 0, 0, 3, 0, 0, 4],
[4, 1, 0, 0, 8, 0, 6, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 9, 5],
[2, 0, 0, 0, 1, 0, 0, 8, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 3, 1, 0, 0, 8, 0, 5, 7]]

grids = [(grid1, 2, 2), (grid2, 2, 2), (grid3, 2, 2), (grid4, 2, 2), (grid5, 2, 2)]
'''
===================================
DO NOT CHANGE CODE ABOVE THIS LINE
===================================
'''
import matplotlib.pyplot as plt
import sys
print(sys.argv)  # Prints the command line arguments as items in a list ['filename.py', 'flag']
explain=False
profile=False
hint=False
hint_explain=False
file=False
global_N=2

'''
For the comment line arguments, variables can be set as False by default, and if they are in the
sys.argv, they're set as True
Later in the code there's functions that can be called which do the flag and we
just need to call them to get them running
'''
if '-explain' in sys.argv and not '-hint' in sys.argv:
    explain=True
if '-hint' in sys.argv and not '-explain' in sys.argv:
    hint=True
if '-explain' in sys.argv and '-hint' in sys.argv:
    hint_explain=True
if '-profile' in sys.argv:
    profile=True
if '-file' in sys.argv:
    file=True    
# Global N will be used later, this represents the Number after the Hint flag
for i in sys.argv:
    if len(i)==1:
        global_N=i
    else:
        global_N=50 #arbitrary large constant

# The profile flag overrides all other flags as they make the code take longer
if profile:
    hint=False
    explain=False
    hint_explain=False
  
def check_section(section, n):
    
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
	n = n_rows*n_cols
	#Make a copy of the original grid
	filled_grid = copy.deepcopy(grid)

	#Loop through the rows
	for i in range(len(grid)):
		#Loop through the columns
		for j in range(len(grid[0])):
			#If we find a zero, fill it in with a random integer
			if grid[i][j] == 0:
				filled_grid[i][j] = random.randint(1, n)

	return filled_grid 

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


# Defining a function that outputs the list of possible values left for any coordinat
def possible_values(grid, row, col, n, n_rows, n_cols):
    ''' 
    This function returns a list of possible values any position can take 
    Args: 
        grid(list) = sudoku grid
        row(int) = x coordinate
        col(int) = y coordinate
        n(int) = max value the number can be
        n_rows(int) = width of subgrid
        n_cols(int) = height of subgrid

    Returns:
        p_values(list) = list of possible values

    '''

    # Find values already present in the sudoku
    row_values = grid[row]
    col_values = [grid[i][col] for i in range(n)]
    subgrid = get_subgrid(row, col)
    square_values = get_squares(grid, n_rows, n_cols)[subgrid]
    # All values 1 to n are possible before we check the rows, columns and squares
    possible_values = set(range(1, n+1))
    # Remove values already present in the row, column, and subgrid
    values_present = set(row_values + col_values + square_values)
    p_values = list(possible_values - values_present)
    return p_values



def find_lowest_possibilites(grid,n,n_rows,n_cols):
    '''
This function will return the coordinates of the positions with the lowest amount of possibilites
    Args: 
        grid(list) = sudoku grid
        n(int) = max value the number can be
        n_rows(int) = width of subgrid
        n_cols(int) = height of subgrid
    Returns:
        An ordered list of possible values and their corresponding coordinates
        ordered from lowest amount of possible values first
        It outputs a list in the form of: [possible value(s)],coordiantes(x,y)
'''
    possible_list=[]
    for i in range(len(zeros_index(grid))):
        row=zeros_index(grid)[i][0]
        col=zeros_index(grid)[i][1]
        # Finding the coordinates of the 0's
        possible_list.append((possible_values(grid,row,col,n,n_rows,n_cols),row,col))
        # Adding to the list the possible values, and the row and column theryre in
    
    return sorted(possible_list)

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

def count_zeros(grid):
    """Count the number of zeros in a list."""
    count = 0
    for row in grid:
        for value in row:
            if value == 0:
                count += 1
    return count
def file(INPUT,OUTPUT):
     pass

def get_times(solver,grid,n_rows, n_cols):
    start_time = time.time()
    solution = solver(grid, n_rows, n_cols)
    elapsed_time = time.time() - start_time
    return elapsed_time


def flag_profile(grid, n_rows, n_cols):
    '''
    This function compares the different solvers' performance on different grids
    '''
    times=[]
    solvers=[random_solve,old_recursive_solve,recursive_solve]
    labels=['Random', 'Old Recursive', 'Recursive']
    for solver in solvers:
        times.append(get_times(solver, grid, n_rows, n_cols))
    print(times,'TIMES')
    plt.bar(labels, times)
    plt.ylabel('Time (seconds)')
    plt.title('Solver time for different algorithms')
    plt.show()

    return times




print(flag_profile(grid5, 2,2))

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



def flag_hint(grid,n_rows,n_cols,N):
    '''Function that puts back a certain number of zeros into the finished grid,
    Returning the somewhat finished grid
    Also if the hint_explain boul gets called then the function will output
    N lines of the explain function
    
    args: grid,n_rows,n_cols
    N (int)= The global N, the number after the hint flag
    returns: The partially filled answer, and if hint_explain is called, then also the 
    partially included explanation
    '''
    N=int(N)
    # getting the coordinates of the zeros
    zeros=zeros_index(grid)
    # Only keeping N elements from the list
    del zeros[:N]
    # Getting the solved grid
    answer=recursive_solve(grid, n_rows, n_cols)
    for coord in zeros:
        # Replacing N solved numbers from the end with 0
        row = coord[0]
        col = coord[1]
        answer[row][col] = 0
    # Outputting N explanation lines
    if hint_explain:
        explained=flag_explain(grid, answer)
        for i in range(N):
            explained_list=explained[:N]
    # if no hint_explain, just return normal partially filled grid
        return answer,explained_list
    return answer



def old_recursive_solve(grid, n_rows, n_cols):
	'''
	This the unimproved function uses recursion to exhaustively search all possible solutions to a grid
	until the solution is found
    This function is purely here for the -profile flag

	args: grid, n_rows, n_cols
	return: A solved grid (as a nested list), or None
	'''

	#N is the maximum integer considered in this board
	n = n_rows*n_cols
	#Find an empty place in the grid
	empty = find_empty(grid)

	#If there's no empty places left, check if we've found a solution
	if not empty:
		#If the solution is correct, return it.
		if check_solution(grid, n_rows, n_cols):
			return grid 
		else:
			#If the solution is incorrect, return None
			return None
	else:
		row, col = empty 

	#Loop through possible values
	for i in range(1, n+1):

			#Place the value into the grid
			grid[row][col] = i
			#Recursively solve the grid
			ans = recursive_solve(grid, n_rows, n_cols)
			#If we've found a solution, return it
			if ans:
				return ans 

			#If we couldn't find a solution, that must mean this value is incorrect.
			#Reset the grid for the next iteration of the loop
			grid[row][col] = 0 

	#If we get here, we've tried all possible values. Return none to indicate the previous value is incorrect.
	return None
def recursive_solve(grid, n_rows, n_cols):
    '''
    This function uses recursion to exhaustively search all possible solutions to a grid
    until the solution is found
    args: grid, n_rows, n_cols
    return: A solved grid (as a nested list), or None
    '''
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
    #     return flag_hint(grid, n_rows, n_cols, global_N)
    # return random_solve(grid, n_rows, n_cols)
    return recursive_solve(grid, n_rows, n_cols)



# If the -explain flag is triggered, output the instructions for each grid
if explain:
    for i in range(len(grids)):
        print('For grid[{}]: {}'.format(i+1, flag_explain(grids[i][0], recursive_solve(grids[i][0], grids[i][1], grids[i][2]))))
'''I need to look at the format of how they will be inputting the new grids, as this is geared towards the
current grids on this file, not the new ones'''
if profile:
    print(flag_profile(grid5, 2, 2),'Profile is working')

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
            print(flag_hint(grid, n_rows, n_cols, global_N))
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
