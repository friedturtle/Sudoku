# A program that solves and displays a given soduku puzzle
# The grid will be represented by a matrix (list of lists)

FULL_SET = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# 9 x 9 grid
base = [[FULL_SET[:] for i in range(9)] for j in range(9)]


def choose_puzzle():
    # Read the puzzle from a file and generate our initial grid
    confirmed = []
    with open("puzzles.txt") as puzzles:
        # Ask which puzzle to use
        print("Choose a puzzle: enter an integer between 1 and 50 inclusive : ")
        puzzleno = int(input())
        puzzle_line = (puzzleno - 1) * 10
        row_num = 0
        starting_grid = puzzles.read().splitlines()[puzzle_line:puzzle_line + 10]
        print(starting_grid[0])
        for i in range(1, 10):
            row = starting_grid[i]
            for k in range(0, len(row)):
                if int(row[k]) != 0:
                    base[row_num][k] = int(row[k])
                    confirmed.append((row_num, k))
            row_num += 1
    return confirmed, puzzleno


def solve_puzzle(solved_squares):
    # Solve the puzzle
    # For each confirmed element, eliminate the possibility of this element occuring
    # in the same ROW, COLUMN and GRID
    solved = False
    debug_counter = 0
    print(solved_squares)

    while not solved:
        for pos in solved_squares:
            print("Pos = ", pos)
            debug_counter += 1
            try:
                value = int(base[pos[0]][pos[1]])
            except TypeError:
                print("TYPE ERROR")
                print("Pos = ", pos, "Attempted value = ", base[pos[0]][pos[1]])
            ####print("Value = ", value)
            # Eliminate from row and column
            for k in range(0, 9):
                ####print("checking... ( ", pos[0], ",", k, ") :   ", base[pos[0]][k])
                if isinstance(base[pos[0]][k], list):
                    if len(base[pos[0]][k]) == 1:
                        base[pos[0]][k] = base[pos[0]][k][0]
                        print("Confirmed at ", pos[0], k, "With : ", base[pos[0]][k])
                        solved_squares.append((pos[0], k))
                        print(solved_squares)
                        ####print(solved_squares)
                        ####print(solved_squares[-1])
                        continue
                    try:
                        base[pos[0]][k].remove(value)
                    except ValueError:
                        pass
                else:
                    ####print("Not a list")
                    pass

            for p in range(0, 9):
                if isinstance(base[p][pos[1]], list):
                    if len(base[p][pos[1]]) == 1:
                        base[p][pos[1]] = base[p][pos[1]][0]
                        print("Confirmed at ", p, pos[1], "With : ", base[p][pos[1]])
                        solved_squares.append((p, pos[1]))
                        print(solved_squares)
                        continue
                    try:
                        base[p][pos[1]].remove(value)
                    except ValueError:
                        pass
            # Grid eliminate
            # Start from the first spot with %3 == 0 to the left
            grid_checker = [-1, -1]
            for m in range(0, 2):
                grid_checker[m] = pos[m]
                while grid_checker[m] % 3 != 0:
                    grid_checker[m] -= 1
            grid_corner = grid_checker[:]
            ####print("pos = ", pos, "Grid corner = ", grid_checker)
            for i in range(0, 3):
                grid_checker[0] = grid_corner[0] + i
                if grid_checker[0] == pos[0]:
                    continue
                else:
                    for j in range(0, 3):
                        grid_checker[1] = grid_corner[1] + j
                        if grid_checker[1] == pos[1]:
                            ####print("Skipping column at j = ", j)
                            continue
                        else:
                            ####print("Grid check at: ", grid_checker, "j = ", j)
                            try:
                                pass
                                ####print(base[grid_checker[0]][grid_checker[1]])
                            except IndexError:
                                print("ERROR grd chk: ", grid_checker)

                            if isinstance(base[grid_checker[0]][grid_checker[1]], list) and len(base[grid_checker[0]][grid_checker[1]]) == 1:
                                # Confirm
                                base[grid_checker[0]][grid_checker[1]] = base[grid_checker[0]][grid_checker[1]][0]
                                solved_squares.append((grid_checker[0], grid_checker[1]))
                            elif isinstance(base[grid_checker[0]][grid_checker[1]], list):
                                try:
                                    base[grid_checker[0]][grid_checker[1]].remove(value)
                                    # If the length is now 1 we have a new confirmed spot for pos
                                    if len(base[grid_checker[0]][grid_checker[1]]) == 1:
                                        print("New confirmed spot at:", grid_checker)
                                        base[grid_checker[0]][grid_checker[1]] = base[grid_checker[0]][grid_checker[1]][0]
                                        print("Value Saved = ", base[grid_checker[0]][grid_checker[1]])
                                        solved_squares.append((grid_checker[0], grid_checker[1]))

                                except ValueError:
                                    pass

                    ####print("Grid check complete at :", grid_checker)
                ####print("Number solved: ", len(solved_squares))
        # Need to use the reverse elimination technique if no new squares have been confirmed
        # Farm this out to a function
        check_empty_squares(solved_squares)
        # This will stop when it confirms one space
        debug_counter += 1
        if len(solved_squares) == 81:
            solved = True
        elif debug_counter > 1500:
            print(base)
            return 0


def write_puzzle(puzzle_number):
    # Save the completed grid to a text file
    with open("solution_test.txt", 'a+') as answer_test:
        # Print the base
        head = "Solution " + str(puzzle_number) + "\n"
        answer_test.write(head)
        for i in range(0, 9):
            for k in range(0, 9):
                answer_test.write(str(base[i][k]))
            answer_test.write("\n")

    pass


def reverse_elimination(r, c, element):
    # Given a square check if each element occurs only once in R / C / G
    # If elemement occurs more than once does it only occur in the current G
    # If so eliminate from other squares in the grid

    # Return true if element occurs only once (here) in row
    counter = 0
    sweep_grid = True
    grid_checker = [r, c]
    for m in range(0, 2):
        while grid_checker[m] % 3 != 0:
            grid_checker[m] -= 1
    grid_corner = grid_checker[:]
    for i in range(0, 9):
        if isinstance(base[r][i], list) and element in base[r][i]:
            counter += 1
            # Is this ocurence outside the current grid?
            if i < grid_corner[1] or i > grid_corner[1] + 2:
                # Outside current grid
                sweep_grid = False
    if counter == 1:
        return 1
    elif sweep_grid:
        # Eliminate the element from all squares in the current G not included in C
        for s in range(0, 3):
            if grid_corner[0] + s == r:
                continue
            else:
                for l in range(0, 3):
                    grid_checker = [grid_corner[0] + s, grid_corner[1] + l]
                if isinstance(base[grid_checker[0]][grid_checker[1]], list) and element in base[grid_checker[0]][grid_checker[1]]:
                    base[grid_checker[0]][grid_checker[1]].remove(element)
                    print("SW GRD ROW Removed: {number} from {spot}".format(number=element, spot=grid_checker))
                    print("Left with: ", base[grid_checker[0]][grid_checker[1]])
                    joke = 0

    # Return true if element occurs only once in column
    counter = 0
    sweep_grid = True
    grid_checker = [r, c]
    for m in range(0, 2):
        while grid_checker[m] % 3 != 0:
            grid_checker[m] -= 1
    grid_corner = grid_checker[:]
    for k in range(0, 9):
        if isinstance(base[k][c], list) and element in base[k][c]:
            counter += 1
            # Is this ocurence outside the current grid?
            if k < grid_corner[0] or k > grid_corner[0] + 2:
                # Outside current grid
                sweep_grid = False
    if counter == 1:
        return 1
    elif sweep_grid:
        # Eliminate the element from all squares in the current G not included in R
        for s in range(0, 3):
                for l in range(0, 3):
                    if grid_corner[1] + l == c:
                        continue
                    else:
                        grid_checker = [grid_corner[0] + s, grid_corner[1] + l]
                        if isinstance(base[grid_checker[0]][grid_checker[1]], list) and element in base[grid_checker[0]][grid_checker[1]]:
                            base[grid_checker[0]][grid_checker[1]].remove(element)
                            print(" GRD SWP COL Removed: {number} from {spot} started with r= {row} c = {col}".format(number=element, spot=grid_checker, row=r, col=c))
                            print("Left with: ", base[grid_checker[0]][grid_checker[1]])

    # Return true if element occurs only once in grid
    counter = 0
    grid_checker = [r, c]
    for m in range(0, 2):
        while grid_checker[m] % 3 != 0:
            grid_checker[m] -= 1
    grid_corner = grid_checker[:]
    # Have grid corner, now check all the lists in the grid
    row_to_sweep = -1
    col_to_sweep = -1
    sweep_row = True
    sweep_col = True
    for s in range(0, 3):
        for l in range(0, 3):
            grid_checker = [grid_corner[0] + s, grid_corner[1] + l]
            if isinstance(base[grid_checker[0]][grid_checker[1]], list) and element in base[grid_checker[0]][grid_checker[1]]:
                counter += 1
                # If the element only occurs in the grid in a R or C then sweep the rest of that R/C
                if counter == 1:
                    row_to_sweep = grid_checker[0]
                    col_to_sweep = grid_checker[1]
                if counter > 1:
                    if grid_checker[0] != row_to_sweep:
                        sweep_row = False
                    if grid_checker[1] != col_to_sweep:
                        sweep_col = False
    if sweep_col and sweep_row:
        sweep_row = False
        sweep_col = False
    if counter == 1:
        return 1
    elif sweep_row:
        # Sweep row
        # Eliminate element from every list in the row NOT in the grid
        for i in range(0, 8):
            if (i >= grid_corner[1]) and (i <= grid_corner[1] + 2):
                pass
            elif isinstance(base[row_to_sweep][i], list) and element in base[row_to_sweep][i]:
                # Eliminate element
                base[row_to_sweep][i].remove(element)
                print("Sw ROW Removed", element, " from", (row_to_sweep, i))
    elif sweep_col:
        # Sweep column
        # Eliminate element from every list in the column NOT in the grid
        for i in range(0, 8):
            if (i >= grid_corner[0]) and (i <= grid_corner[0] + 2):
                pass
            elif isinstance(base[i][col_to_sweep], list) and element in base[i][col_to_sweep]:
                # Eliminate element
                base[i][col_to_sweep].remove(element)
                print("Sw COL Removed", element, " from", (i, col_to_sweep))
    # If we haven't returned true by now we can NOT confirm element belongs in base[r][c]
    return 0


def naked_pairs(start_row, start_col):
    print("RUNNING MATCHING SET")
    # Check the other squares in the column and grid
    counter = 0
    checker = [start_row, start_col]
    while checker[0] % 3 != 0:
        checker[0] -= 1
    for i in range(0,3):
        if base[checker[0]][checker[1]] == base[start_row][start_col]:
            counter += 1
            if counter > length_set:
                break
        checker[0] += 1
    if counter == length_set:
        checker[0] -= 3
        # Eliminate the matching set from the rest of the C
        for set_element in base[start_row][start_col]:
            for k in range(0, 8):
                if (k >= checker[0]) and (k <= checker[0] + 2):
                    pass
                elif isinstance(base[k][start_col], list) and set_element in base[k][start_col]:
                    # Eliminate element
                    base[k][start_col].remove(set_element)
                    print("Match set COL Removed", set_element, " from", (k, start_col))
        # Also eliminate from rest of grid
        return 1

    # Check the other squares in the row and grid
    counter = 0
    checker = [start_row, start_col]
    while checker[1] % 3 != 0:
        checker[1] -= 1
    for i in range(0, 3):
        if base[checker[0]][checker[1]] == base[start_row][start_col]:
            counter += 1
            if counter > length_set:
                break
        checker[1] += 1
    if counter == length_set:
        checker[1] -= 3
        # Eliminate the matching set from the rest of the C
        for set_element in base[start_row][start_col]:
            for l in range(0, 8):
                if (l >= checker[1]) and (l <= checker[1] + 2):
                    pass
                elif isinstance(base[start_row][l], list) and set_element in base[start_row][l]:
                    # Eliminate element
                    base[start_row][l].remove(set_element)
                    print("Match set ROW Removed", set_element, " from", (start_row, l))
        # Also eliminate from rest of grid
        return 1
    return 0


def check_empty_squares(filled_squares):
    # Pick a square (that contains a list)
    for row in range(0, 9):
        for column in range(0, 9):
            if isinstance(base[row][column], list):
                if len(base[row][column]) == 1:
                    base[row][column] = base[row][column][0]
                    filled_squares.append((row, column))
                    print("confirming single value list pos = ", (row, column), "value = ", base[row][column])
                    continue
                # Determine if each possibility occurs only once in R/C/G
                for possibility in base[row][column]:
                    # Reverse eliminate
                    # if it returns 1 we have confirmed a new space at [row column]
                    if reverse_elimination(row, column, possibility):
                        base[row][column] = possibility
                        filled_squares.append((row, column))
                        print("Reverse Elimination Filled", (row, column), "With: ", possibility)
                        # Success! return 1
                        return 1
                # Call a function to deal with matching sets of 2 or 3 values in the same G and R/C
                if len(base[row][column]) == 2 or len(base[row][column]) == 3:
                    # Check for matching sets
                    naked_pairs(row, column)

    return 0







def user_puzzle():
    # Allow the user to enter an incomplete grid
    pass
    # Determine if this is a valid puzzle

    # Save this grid to the list of puzzles


def main():
    (confirmed, puzzleno) = choose_puzzle()
    solve_puzzle(confirmed)
    write_puzzle(puzzleno)


main()
