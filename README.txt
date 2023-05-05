# FCP-COURSEWORK 3

To solve the 7 grids within the 'coursework3.py' file, run the main function in terminal without the -file flag. The grid solutions and the time taken to solve each grid will be printed.

To read and solve a grid from another file, run the main function in terminal with the -file flag, followed by 'inputfile.txt' 'outputfile.txt'. The sudoku grid from your 'inputfile.txt' will be solved by the new recursive solver, and the soltion will be printed to your 'outputfile.txt'

Enter the -profile flag in terminal to produce a graph plotting the performance of our solver in the form of a bar graph. The -profile will output plots when the -file flag is NOT present, as it cannot output plots to .txt files.

Enter the -hint N flag (where N is the number of squares you want solved), and the grid with N values filled in will be returned. If you use the -hint N flag alongside the -file flag, the grid from the input file with N squares filled in will be printed to the output file. The -hint N flag also works alongside the -explain flag.

Enter the -explain flag in terminal to print the answer of a grid, as well as a list of instructions for solving the puzzle. If you enter the -explain flag alongside the -file flag, the completed grid from the input file will be printed in the output file, along with the list of instructions for solving the puzzle

For the wavefront propagation solver, you will need to open the coursework.py file and put in the grid you want solved and input the possible values into the empty locations in the unsolved grid.

NOTE: This program appears to only run succesfully through terminal on MAC. The cause of this issue is unknown.
