# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the warehouse domain.

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools


def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.


       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board

       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists

       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]


       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.

       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''

    n_grid = initial_tenner_board[0]
    last_row = initial_tenner_board[1]
    num_rows = len(n_grid)
    num_cols = len(last_row)

    var_grid = create_var_grid(n_grid, num_cols, num_rows)

    all_bin_cons = []  # add all constraints in a list, one constraint per cell

    # Create binary row constraints and add to list of all constraints
    for i in range(num_rows):
        for j in range(num_cols):
            for k in range(j+1, num_cols):
                # Check for repeating values within the row using helper
                all_bin_cons += cons_valid_combos(
                    var_grid[i][j], var_grid[i][k])

    # Create binary adjacency constraints to add to list of all constraints
    binary_adj_cons(all_bin_cons, var_grid, num_rows, num_cols)

    # Create sum constraints to add to list of all constraints
    nary_sum_cons(all_bin_cons, var_grid, last_row, num_rows, num_cols)

    # return csp_setup("tenner_model1", all_bin_cons, var_grid, num_rows, num_cols), var_grid
    return None, None
##############################


def csp_setup(name, all_cons, var_grid, num_rows, num_cols):
    csp = CSP(name)
    for i in range(num_rows):
        for j in range(num_cols):
            csp.add_var(var_grid[i][j])
    for cons in all_cons:
        csp.add_constraint(cons)
    return csp


def create_var_grid(n_grid, num_cols, num_rows):
    # Helper function to create the grid of variables according to tenner grid specs
    var_grid = []
    for i in range(num_rows):
        row = []
        # Create var for each element in row
        for j in range(num_cols):
            if n_grid[i][j] != -1:
                # Can only take the defined value
                values_ij = [n_grid[i][j]]
            else:
                # Can be any value
                values_ij = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            var = Variable(str(i)+str(j), values_ij)
            row.append(var)
        var_grid.append(row)
    return var_grid


def cons_valid_combos(var1, var2):
    # Helper function to set up valid tuples in a constraint, returns
    valid_combs = []
    cons = Constraint("c", [var1, var2])
    # Check for repeating values
    for comb in itertools.product(var1.cur_domain(), var2.cur_domain()):
        if comb[0] != comb[1]:
            valid_combs.append(comb)
    cons.add_satisfying_tuples(valid_combs)
    return [cons]


def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.

       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary 
       all-different constraints: all-different constraints for the variables in
       each row, contiguous cells (including diagonally contiguous cells), and 
       sum constraints for each column. Each of these constraints is over more 
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''

    n_grid = initial_tenner_board[0]
    last_row = initial_tenner_board[1]
    num_rows = len(n_grid)
    num_cols = len(last_row)

    var_grid = create_var_grid(n_grid, num_cols, num_rows)
    all_cons = []

    # Create n-ary row constraints
    for i in range(num_rows):
        scope = []
        possible_dom = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        # Check var values to identify scope
        for j in range(num_cols):
            if n_grid[i][j] == -1:
                scope.append(n_grid[i][j])
            else:
                possible_dom.remove(n_grid[i][j])

        row_cons = Constraint("c", scope)
        valid_set = []
        for perm in itertools.permutations(possible_dom):
            valid_set.append(perm)
        row_cons.add_satisfying_tuples(valid_set)
        all_cons.append(row_cons)

    # Create binary adjacency constraints to add to list of all constraints
    binary_adj_cons(all_cons, var_grid, num_rows, num_cols)

    # Create sum constraints to add to list of all constraints
    nary_sum_cons(all_cons, var_grid, last_row, num_rows, num_cols)

    return csp_setup("tenner_model2", all_cons, var_grid, num_rows, num_cols), var_grid


def binary_adj_cons(all_cons, var_grid, num_rows, num_cols):
    # Helper function to create binary adjacency constraints
    for i in range(num_rows-1):
        for j in range(num_cols):
            # Adj element below check
            all_cons += cons_valid_combos(
                var_grid[i][j], var_grid[i+1][j])
            # Adj left diag element below check
            if j != 0:
                all_cons += cons_valid_combos(
                    var_grid[i][j], var_grid[i+1][j-1])
            # Adj right diag element below check
            if j != num_cols-1:
                all_cons += cons_valid_combos(
                    var_grid[i][j], var_grid[i+1][j+1])


def nary_sum_cons(all_cons, var_grid, last_row, num_rows, num_cols):
    # Helper function to create n-ary sum constraints
    for col in range(num_cols):
        scope = []
        vars_doms = []
        for row in range(num_rows):
            # Create list of scope of variables and list of their domains for sum constraint
            scope.append(var_grid[row][col])
            vars_doms.append(var_grid[row][col].cur_domain())
        sum_cons = Constraint("c", scope)
        # Check if sum of this set of values is valid
        valid_sums = []
        for val_set in itertools.product(*vars_doms):
            if sum(val_set) == last_row[col]:
                valid_sums.append(val_set)
        sum_cons.add_satisfying_tuples(valid_sums)
        all_cons.append(sum_cons)
