# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete problem solution.
'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''


def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    # IMPLEMENT
    pruned_vals = []

    # Create the constraints depending whether newVar is defined
    if newVar is None:
        constraints = csp.get_all_cons()
    else:
        constraints = csp.get_cons_with_var(newVar)

    for cons in constraints:
        # Check if there is just 1 variable unassigned in the constraint
        if cons.get_n_unasgn() == 1:

            unasgn_var = cons.get_unasgn_vars()[0]
            domain = unasgn_var.cur_domain()
            # Loop through the variable's domain checking if each value is valid
            for val in domain:
                check = (unasgn_var, val)
                if not cons.has_support(unasgn_var, val) and check not in pruned_vals:
                    # If not valid then add to list of pruned values
                    pruned_vals.append(check)
                    unasgn_var.prune_value(val)

                    if unasgn_var.cur_domain_size == 0:
                        return False, pruned_vals

    return True, pruned_vals


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    # IMPLEMENT
    pruned_vals = []

    # Create GAC queue depending if newVar is defined
    if newVar is None:
        gac_q = csp.get_all_cons()
    else:
        gac_q = csp.get_cons_with_var(newVar)
    # Loop through and process all constraints in the queue
    while gac_q:
        cons = gac_q.pop(0)

        for var in cons.get_scope():
            domain = var.cur_domain()
            # Each variable in the constraint must have its domain checked
            for val in domain:
                check = (var, val)
                if not cons.has_support(var, val) and check not in pruned_vals:
                    # If a value in the domain is not valid, it gets pruned
                    pruned_vals.append(check)
                    var.prune_value(val)

                    if var.cur_domain_size == 0:
                        return False, pruned_vals
                    else:
                        # Check for all constraints containing this variable and add them to the queue
                        for cons_w_var in csp.get_cons_with_var(var):
                            if cons_w_var not in gac_q:
                                gac_q.append(cons_w_var)

    return True, pruned_vals


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    smallest = float('inf')
    ret_var = None
    all_vars = csp.get_all_vars()

    for var in all_vars:
        if smallest > var.cur_domain_size():
            smallest = var.cur_domain_size()
            ret_var = var
    return ret_var
