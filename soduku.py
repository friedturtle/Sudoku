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
        puzzle_line = (int(input()) - 1) * 10
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
    return confirmed


def solve_puzzle(solved_squares):
    # Solve the puzzle
    # For each confirmed element, eliminate the possibility of this element occuring
    # in the same ROW, COLUMN and GRID
    solved = False
    while not solved:
        for pos in solved_squares:
            value = int(base[pos[0]][pos[1]])
            print("Value = ", value)
            # Eliminate from row and column
            for k in range(0, 9):
                #print("checking... ( ", pos[0], ",", k, ") :   ", base[pos[0]][k])
                if isinstance(base[pos[0]][k], list):
                    if len(base[pos[0]][k]) == 1:
                        base[pos[0]][k] = base[pos[0]][k][0]
                        print("Confirmed at ", pos[0], k)
                        solved_squares.append((pos[0], k))
                        print(solved_squares)
                        print(solved_squares[-1])
                        continue
                    try:
                        base[pos[0]][k].remove(value)
                    except ValueError:
                        pass
                else:
                    #print("Not a list")
                    pass
                if isinstance(base[k][pos[1]], list):
                    if len(base[k][pos[1]]) == 1:
                        base[k][pos[1]] = base[k][pos[1]][0]
                        print("Confirmed at ", k, pos[1])
                        solved_squares.append((k, pos[1]))
                        continue
                    try:
                        base[k][pos[1]].remove(value)
                    except ValueError:
                        pass

            # Grid eliminate
            # Start from the first spot with %3 == 0 to the left
            grid_checker = [-1, -1]
            for m in range(0,2):
                grid_checker[m] = pos[m]
                while grid_checker[m]%3 != 0:
                    grid_checker[m] -= 1
            grid_corner = grid_checker[:]
            print("pos = ", pos, "Grid corner = ", grid_checker)
            for i in range(0, 3):
                grid_checker[0] = grid_corner[0] + i
                if grid_checker[0] == pos[0]:
                    grid_checker[0] += 1
                    continue
                else:
                    for j in range(0, 3):
                        grid_checker[1] = grid_corner[1] + j
                        if grid_checker[1] == pos[1]:
                            print("Skipping column at j = ", j)
                            continue
                        else:
                            print("Grid check at: ", grid_checker, "j = ", j)
                            try:
                                print(base[grid_checker[0]][grid_checker[1]])
                            except IndexError:
                                print("ERROR grd chk: ", grid_checker)

                            if isinstance(base[grid_checker[0]][grid_checker[1]], list):
                                try:
                                    base[grid_checker[0]][grid_checker[1]].remove(value)
                                    # If the length is now 1 we have a new confirmed spot for pos
                                    if len(base[grid_checker[0]][grid_checker[1]]) == 1:
                                        print("New confirmed spot at:", grid_checker)
                                        base[grid_checker[0]][grid_checker[1]] = base[grid_checker[0]][grid_checker[1]][0]
                                        print("Value Saved = ", base[grid_checker[0]][grid_checker[1]])
                                        solved_squares.append(grid_checker)

                                except ValueError:
                                    pass

                    print("Grid check complete at :", grid_checker)

        if len(solved_squares) == 81:
            solved = True



def write_puzzle():
    # Save the completed grid to a text file
    pass

def user_puzzle():
    # Allow the user to enter an incomplete grid
    pass

    # Save this grid to the list of puzzles


def main():
    confirmed = choose_puzzle()
    solve_puzzle(confirmed)
    print(confirmed)







main()