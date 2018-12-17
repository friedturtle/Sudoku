# A program that solves and displays a given soduku puzzle
# The grid will be represented by a matrix (list of lists)

FULL_SET = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# 9 x 9 grid
base = [[FULL_SET[:] for i in range(9)] for j in range(9)]


def choose_puzzle(number):
    # Read the puzzle from a file and generate our initial grid
    confirmed = []
    with open("puzzles.txt") as puzzles:
        puzzleno = number
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

def sweep_house(elements, position, exceptions, mode):

    # For row and column mode position is a len = 1 integer list and exceptions is lists of integers (0 - 8)
    if mode == "row" or "column":
        for i in range(0, 9):
            if i not in exceptions:
                for element in elements:
                    if mode == "row":
                        current_square = base[position[0]][i]
                    elif mode == "column":
                        current_square = base[i][position[0]]
                    else:
                        return 1

                    if isinstance(current_square, list) and element in current_square:
                        current_square.remove(element)

    # For grid mode position is a len = 2 list and exceptions is a list of len = 2 lists
    elif mode == "grid":
        grid_checker = position
        for m in range(0, 2):
            while grid_checker[m] % 3 != 0:
                grid_checker[m] -= 1
        grid_corner = grid_checker[:]
        for s in range(0, 3):
            for k in range(0, 3):
                grid_checker = [grid_corner[0] + s, grid_corner[1] + k]
                current_square = base[grid_checker[0]][grid_checker[1]]
                if grid_checker not in exceptions:
                    if isinstance(current_square, list):
                        for element in elements:
                            if element in current_square:
                                current_square.remove(element)
    else:
        return 1










def solve_puzzle(solved_squares):
    # Solve the puzzle
    # For each confirmed element, eliminate the possibility of this element occuring
    # in the same ROW, COLUMN and GRID
    solved = False
    debug_counter = 0
    print(solved_squares)

    while not solved:
        for pos in solved_squares:
            ####print("Pos = ", pos)
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
        if debug_counter % 5 == 0:
            naked_sets()


        if debug_counter % 10 == 0:
            hidden_pairs()

        if len(solved_squares) == 81:
            solved = True
        elif debug_counter > 2500:
            print("DEBUG COUNTER")
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


def naked_sets():
    # Check the entire base for naked pairs, triples and quads
    # This doesnt account for disjointed naked triples and quads
    # Check rows
    for i in range(0, 9):
        # Store the positions where the number of candidates is 4,3,2
        pos_of_lengths = [[], [], []]
        for k in range(0, 9):
            if isinstance(base[i][k], list) and 2 <= len(base[i][k]) <= 4:
                number_candidates = len(base[i][k])
                # To assign to correct index idx = - length + 4
                length_index = 4 - number_candidates
                pos_of_lengths[length_index].append(k)
        # Check if there are enough of the right length to resolve naked sets
        for m in range(0, 3):
            match_count = 0
            if len(pos_of_lengths[m]) == 4 - m:
                # Test if they are matching sets
                sets_already_tested = []
                for test_col_pos in pos_of_lengths[m]:
                    test_set = base[i][test_col_pos]
                    if test_set not in sets_already_tested:
                        for col_pos in pos_of_lengths[m]:
                            if base[i][col_pos] == test_set:
                                match_count += 1
                                if match_count == 4 - m:
                                    # We have a naked set. Resolve it and edit pos of lengths
                                    for k in range(0, 9):
                                        if isinstance(base[i][k], list) and base[i][k] != test_set:
                                            for candidate in test_set:
                                                if candidate in base[i][k]:
                                                    if 2 <= len(base[i][k]) <= 4:
                                                        pos_of_lengths[4 - len(base[i][k])].remove(k)
                                                        if len(base[i][k]) > 2:
                                                            pos_of_lengths[5 - len(base[i][k])].append(k)
                                                    base[i][k].remove(candidate)
                                                    if len(base[i][k]) == 4:
                                                        pos_of_lengths[0].append(k)
                                                    print("NAKED row removed", candidate, "from", [i, k], "left with",
                                                          base[i][k])
                                                    print(pos_of_lengths)
                            else:
                                pass
                        sets_already_tested.append(test_set)
                        match_count = 0
    # Check columns
    for k in range(0, 9):
        # Store the positions where the number of candidates is 4,3,2
        pos_of_lengths = [[], [], []]
        for i in range(0, 9):
            if isinstance(base[i][k], list) and 2 <= len(base[i][k]) <= 4:
                number_candidates = len(base[i][k])
                # To assign to correct index idx = - length + 4
                length_index = 4 - number_candidates
                pos_of_lengths[length_index].append(i)
        # Check if there are enough of the right length to resolve naked sets
        for m in range(0, 3):
            match_count = 0
            if len(pos_of_lengths[m]) == 4 - m:
                sets_already_tested = []
                # Test if they are matching sets
                for test_row_pos in pos_of_lengths[m]:
                    test_set = base[test_row_pos][k]
                    if test_set not in sets_already_tested:
                        for row_pos in pos_of_lengths[m]:
                            if base[row_pos][k] == test_set:
                                match_count += 1
                                if match_count == 4 - m:
                                    # We have a naked set. Resolve it and end the function
                                    for i in range(0, 9):
                                        if isinstance(base[i][k], list) and base[i][k] != test_set:
                                            for candidate in test_set:
                                                if candidate in base[i][k]:
                                                    base[i][k].remove(candidate)
                                                    print("NAKED col removed", candidate, "from", [i, k], "left with",
                                                          base[i][k])
                                    return 1
                            else:
                                pass
                    sets_already_tested.append(test_set)
                    match_count = 0

    # Check grids
    grid_corner = [-1, -1]
    for s in range(0, 3):
        grid_corner[0] = s * 3
        for l in range(0, 3):
            grid_corner[1] = l * 3
            # Grid corner chosen, now start counting candidate occurances
            pos_of_lengths = [[], [], []]
            for r in range(grid_corner[0], grid_corner[0] + 3):
                for c in range(grid_corner[1], grid_corner[1] + 3):
                    if isinstance(base[r][c], list) and 2 <= len(base[r][c]) <= 4:
                        number_candidates = len(base[r][c])
                        length_index = 4 - number_candidates
                        pos_of_lengths[length_index].append([r, c])
            # Check if there are enough of the right length to form naked sets
            for m in range(0, 3):
                match_count = 0
                if len(pos_of_lengths[m]) == 4 - m:
                    sets_already_tested = []
                    for test_grid_pos in pos_of_lengths[m]:
                        test_set = base[test_grid_pos[0]][test_grid_pos[1]]
                        if test_set not in sets_already_tested:
                            for grid_pos in pos_of_lengths[m]:
                                if base[grid_pos[0]][grid_pos[1]] == test_set:
                                    match_count += 1
                                    if match_count == 4 - m:
                                        # We have a naked set. Resolve it and end the function
                                        for r in range(grid_corner[0], grid_corner[0] + 3):
                                            for c in range(grid_corner[1], grid_corner[1] + 3):
                                                if isinstance(base[r][c], list) and base[r][c] != test_set:
                                                    for candidate in test_set:
                                                        if candidate in base[r][c]:
                                                            base[r][c].remove(candidate)
                                                            print("NAKED grid removed", candidate, "from", [r, c], "left with",
                                                                  base[r][c])

                        sets_already_tested.append(test_set)
                        match_count = 0


def new_naked_sets():
    # Rows
    for i in range(0, 9):
        # Store the positions where the number of candidates is 2,3,4
        pos_of_lengths = [[], [], []]
        for k in range(0, 9):
            if isinstance(base[i][k], list) and 2 <= len(base[i][k]) <= 4:
                number_candidates = len(base[i][k])
                # To assign to correct index idx = - length + 4
                length_index = number_candidates - 2
                pos_of_lengths[length_index].append(k)
        # Now we have the positions of squares with lengths 2,3,4 in pos of lengths
        # Start by looking for naked pairs then triples then quads
        for set_length in range(2, 5):
            if set_length == 2:
                # Naked pairs so exact matches
                length_index = set_length - 2
                sets_already_tested = []
                number_sets = len(pos_of_lengths[length_index])
                for test_set_pos_idx in range(0, number_sets):
                    match_count = 0
                    test_set_pos = pos_of_lengths[length_index][test_set_pos_idx]
                    test_set = base[i][test_set_pos][:]
                    if test_set not in sets_already_tested:
                        sets_already_tested.append(test_set)
                        for compare_set_pos_idx in range(test_set_pos_idx, number_sets):
                            compare_set_pos = pos_of_lengths[length_index][compare_set_pos_idx]
                            compare_set = base[i][compare_set_pos]
                            if test_set == compare_set:
                                match_count +=1
                        if match_count == set_length - 1:
                            for k in range(0, 9):
                                if isinstance(base[i][k], list) and base[i][k] != test_set:
                                    for candidate in test_set:
                                        if candidate in base[i][k]:
                                            if 2 <= len(base[i][k]) <= 4:
                                                pos_of_lengths[len(base[i][k]) - 2].remove(k)
                                                if len(base[i][k]) > 2:
                                                    pos_of_lengths[len(base[i][k]) - 3].append(k)
                                            base[i][k].remove(candidate)
                                            if len(base[i][k]) == 4:
                                                pos_of_lengths[2].append(k)
                                            print("NAKED row removed", candidate, "from", [i, k], "left with",
                                                  base[i][k])
                                            print(pos_of_lengths)

            # Naked pairs are handled. Now in to naked triples and quads.
            elif set_length == 3:
                # Set length = 3 then = 4
                # For length = 3 our test sets will come from len 3 and then len = 2 after
                # Our compare sets will come from len = 3 (exact) and then len = 2 (subsets) Done!
                length_index = set_length - 2
                sets_already_tested = []
                number_sets = len(pos_of_lengths[length_index])
                for test_set_pos_idx in range(0, number_sets):
                    match_count = 0
                    test_set_pos = pos_of_lengths[length_index][test_set_pos_idx]
                    test_set = base[i][test_set_pos][:]
                    if test_set not in sets_already_tested:
                        sets_already_tested.append(test_set)
                        for compare_set_pos_idx in range(test_set_pos_idx, number_sets):
                            compare_set_pos = pos_of_lengths[length_index][compare_set_pos_idx]
                            compare_set = base[i][compare_set_pos]
                            if test_set == compare_set:
                                match_count += 1
                        if match_count == set_length - 1:
                            # We have an exact match naked triple. Its enough to stop here and sweep
                            # Need a function to call for sweeping!
                            # CAREFUL WITH CONDITIONS
                            for k in range(0, 9):
                                if isinstance(base[i][k], list) and base[i][k] != test_set:
                                    for candidate in test_set:
                                        if candidate in base[i][k]:
                                            if 2 <= len(base[i][k]) <= 4:
                                                pos_of_lengths[len(base[i][k]) - 2].remove(k)
                                                if len(base[i][k]) > 2:
                                                    pos_of_lengths[len(base[i][k]) - 3].append(k)
                                            base[i][k].remove(candidate)
                                            if len(base[i][k]) == 4:
                                                pos_of_lengths[2].append(k)
                                            print("NAKED row removed", candidate, "from", [i, k], "left with",
                                                  base[i][k])
                                            print(pos_of_lengths)
                        else:
                            # Otherwise consider the len = 2 squares an determine if their elements are in the test set
                            number_sets = len(pos_of_lengths[length_index - 1])
                            for compare_set_pos_idx in range(0, number_sets):
                                compare_set_pos = pos_of_lengths[length_index - 1][compare_set_pos_idx]
                                compare_set = base[i][compare_set_pos]
                                is_compare_set_contained = True
                                for compare_set_element in compare_set:
                                    if compare_set_element in test_set:
                                        pass
                                    else:
                                        is_compare_set_contained = False
                                if is_compare_set_contained:
                                    match_count += 1
                            if match_count == set_length - 1:
                                # Sweep! Be careful with conditions here!
                                for k in range(0, 9):
                                    is_naked_set_contained = True
                                    for element in base[i][k]:
                                        if element in test_set:
                                            pass
                                        else:
                                            is_naked_set_contained = False
                                    if not is_naked_set_contained:
                                        for candidate in test_set:
                                            if candidate in base[i][k]:
                                                if 2 <= len(base[i][k]) <= 4:
                                                    pos_of_lengths[len(base[i][k]) - 2].remove(k)
                                                    if len(base[i][k]) > 2:
                                                        pos_of_lengths[len(base[i][k]) - 3].append(k)
                                                base[i][k].remove(candidate)
                                                if len(base[i][k]) == 4:
                                                    pos_of_lengths[2].append(k)
                                                print("NAKED row removed", candidate, "from", [i, k], "left with",
                                                      base[i][k])
                                                print(pos_of_lengths)

                # Finally consider naked triples where each square only contains 2 elements.
                # The test set is formed from len = 2 squares and one extra element
                # The comparison sets are the rest of the len = 2 squares
                # This may be intensive so only try if there are enough len = 2 squares to form a triple (3)
                # If at any point there are no longer enough squares to for a triple then STOP
                # Are sets already tested still useful here? YES?
                length_index = set_length - 3
                number_sets = len(pos_of_lengths[length_index])
                sets_remaining = number_sets
                if number_sets >= 3:
                    for test_set_pos_idx in range(0, number_sets):
                        match_count = 0
                        test_set_pos = pos_of_lengths[length_index][test_set_pos_idx]
                        # Test set MUST be a COPY because we will be editing it.
                        test_set = base[i][test_set_pos][:]
                        if test_set not in sets_already_tested:
                            for compare_set_pos_idx in range(test_set_pos_idx, number_sets):
                                compare_set_pos = pos_of_lengths[length_index][compare_set_pos_idx]
                                compare_set = base[i][compare_set_pos]
                                # Now look for a single element match to the test set
                                # Add the remaining element to the test set to form a triple and use this to compare.
                                # We wont get an exact match as this was handled by naked pairs
                                is_single_element_match = False
                                if len(test_set) == 2:
                                    for compare_set_element in compare_set:
                                        if compare_set_element in test_set:
                                            is_single_element_match = True
                                        else:
                                            leftover_element = compare_set_element
                                    if is_single_element_match:
                                        test_set.append(leftover_element)
                                        # We have formed our 3 element test set, now compare!
                                        # Looking for one more square that matches the set!
                                        match_count += 1
                                else:
                                    # Full test set already, check if its used already
                                    if test_set not in sets_already_tested:
                                        sets_already_tested.append(test_set)
                                        is_compare_set_contained = True
                                        for compare_set_element in compare_set:
                                            if compare_set_element in test_set:
                                                pass
                                            else:
                                                is_compare_set_contained = False
                                        if is_compare_set_contained:
                                            match_count += 1
                                    if match_count == set_length - 1:
                                        # We have a naked triple! Sweep the row!
                                        for k in range(0, 9):
                                            is_naked_set_contained = True
                                            for element in base[i][k]:
                                                if element in test_set:
                                                    pass
                                                else:
                                                    is_naked_set_contained = False
                                            if not is_naked_set_contained:
                                                for candidate in test_set:
                                                    if candidate in base[i][k]:
                                                        if 2 <= len(base[i][k]) <= 4:
                                                            pos_of_lengths[len(base[i][k]) - 2].remove(k)
                                                            if len(base[i][k]) > 2:
                                                                pos_of_lengths[len(base[i][k]) - 3].append(k)
                                                        base[i][k].remove(candidate)
                                                        if len(base[i][k]) == 4:
                                                            pos_of_lengths[2].append(k)
                                                        print("NAKED row removed", candidate, "from", [i, k],
                                                              "left with",
                                                              base[i][k])
                                                        print(pos_of_lengths)
                                    # If we dont have a triple we continue to the next compare square
                                    # When we reach the end if we dont have a triple with this test set
                                    # We need to create a new one
                                    # Go back and start over by looking for the next single element match
                                    # While loop?
                                    # While no match with this set - do everything...?




                                    # If we dont get a triple with this set we need to pop the leftover element we added
                                    # Then go back and look for another single element match and create a new test set
                                    # BEFORE We move on to a new starting test square!
                                    # But we do want to move on to a new compare set.

                    sets_remaining -= 1



















def hidden_pairs():
    # Check each row of the base for hidden pairs
    for i in range(0, 9):
        # Each list in the list represents an element 1,2,3... the values note the positions it occurs
        counting_elements = [[], [], [], [], [], [], [], [], []]
        twice_indexes = []
        for k in range(0, 9):
            if isinstance(base[i][k], list):
                if len(base[i][k]) == 1:
                    return 1
                else:
                    for candidate in base[i][k]:
                        counting_elements[candidate - 1].append(k)
        # Before we move to the next row resolve any hidden pairs
        for m in range(0, 9):
            if len(counting_elements[m]) == 2:
                # Save this for future comparison
                twice_indexes.append(m)
        # Now compare the positions of the candidates that appear only twice
        for n in range(0, len(twice_indexes) - 1):
            for v in range(n + 1, len(twice_indexes)):
                if counting_elements[n] == counting_elements[v]:
                    # Remove all but (n + 1) and (v + 1) from those spots
                    for col_pos in counting_elements[n]:
                        for candidate in base[i][col_pos]:
                            if candidate != (n + 1) and candidate != (v + 1):
                                base[i][col_pos].remove(candidate)
                                print("HIDDEN Row removed: ", candidate, "from: ", [i, col_pos], " left with: ", base[i][col_pos])
                                print("Hidden pair is: ", (n + 1, v + 1))
    # Check each column of the base for hidden pairs
    for k in range(0, 9):
        # Each list in the list represents an element 1,2,3... the values note the positions it occurs
        counting_elements = [[], [], [], [], [], [], [], [], []]
        twice_indexes = []
        for i in range(0, 9):
            if isinstance(base[i][k], list):
                if len(base[i][k]) == 1:
                    return 1
                else:
                    for candidate in base[i][k]:
                        counting_elements[candidate - 1].append(i)
        # Before we move to the next row resolve any hidden pairs
        for m in range(0, 9):
            if len(counting_elements[m]) == 2:
                # Save this for future comparison
                twice_indexes.append(m)
        # Now compare the positions of the candidates that appear only twice
        for n in range(0, len(twice_indexes) - 1):
            for v in range(n + 1, len(twice_indexes)):
                if counting_elements[n] == counting_elements[v]:
                    # Remove all but (n + 1) and (v + 1) from those spots
                    for row_pos in counting_elements[n]:
                        for candidate in base[row_pos][k]:
                            if candidate != (n + 1) and candidate != (v + 1):
                                base[row_pos][k].remove(candidate)
                                print("HIDDEN Col removed: ", candidate, "from: ", [row_pos, k], " left with: ", base[row_pos][k])
                                print("Hidden pair is: ", (n + 1, v + 1))
                                print("Counting elements: ", counting_elements)
    # Check each grid in the base for hidden pairs
    grid_corner = [-1, -1]
    for s in range(0, 3):
        grid_corner[0] = s * 3
        for l in range(0, 3):
            grid_corner[1] = l * 3
            # Grid corner chosen, now start counting candidate occurances
            counting_elements = [[], [], [], [], [], [], [], [], []]
            twice_indexes = []
            grid_checker = [0, 0]
            for r in range(grid_corner[0], grid_corner[0] + 3):
                grid_checker[0] = r
                for c in range(grid_corner[1], grid_corner[1] + 3):
                    grid_checker[1] = c
                    if isinstance(base[r][c], list):
                        if len(base[r][c]) == 1:
                            return 1
                        else:
                            for candidate in base[r][c]:
                                counting_elements[candidate - 1].append((r, c))
            # Before we move to the next grid resolve any hidden pairs
            for m in range(0, 9):
                if len(counting_elements[m]) == 2:
                    # Save this for future comparison
                    twice_indexes.append(m)
            # Now compare the positions of the candidates that appear only twice
            for n in range(0, len(twice_indexes) - 1):
                for v in range(n + 1, len(twice_indexes)):
                    if counting_elements[n] == counting_elements[v]:
                        # Remove all but (n + 1) and (v + 1) from those spots
                        for grid_pos in counting_elements[n]:
                            for candidate in base[grid_pos[0]][grid_pos[1]]:
                                if candidate != (n + 1) and candidate != (v + 1):
                                    base[grid_pos[0]][grid_pos[1]].remove(candidate)
                                    print("HIDDEN Grid removed: ", candidate, "from: ", grid_pos, " left with: ", base[grid_pos[0]][grid_pos[1]])


def check_empty_squares(filled_squares):
    # Pick a square (that contains a list)
    for row in range(0, 9):
        for column in range(0, 9):
            if isinstance(base[row][column], list):
                if len(base[row][column]) == 1:
                    base[row][column] = base[row][column][0]
                    filled_squares.append((row, column))
                    print("confirming single value list pos = ", (row, column), "value = ", base[row][column])
                    return 1
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

    return 0


def user_puzzle():
    # Allow the user to enter an incomplete grid
    pass
    # Determine if this is a valid puzzle

    # Save this grid to the list of puzzles


def main():
    print("Choose which puzzle to solve (1-50). Enter 0 to solve all puzzles.")
    chosen_number = int(input())
    if chosen_number == 0:
        for i in range(1, 51):
            global base
            base = base = [[FULL_SET[:] for k in range(9)] for j in range(9)]
            (confirmed, puzzle_num) = choose_puzzle(i)
            solve_puzzle(confirmed)
            write_puzzle(puzzle_num)
    else:
        (confirmed, puzzle_num) = choose_puzzle(chosen_number)
        solve_puzzle(confirmed)
        write_puzzle(puzzle_num)


main()
