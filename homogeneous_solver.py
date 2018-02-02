from sympy import roots

from sympy.parsing.sympy_parser import parse_expr

import util


# Transform the given homogeneous recurrence relation to a closed formula.
def solve_eq(init_conditions, associated):
    degree = len(init_conditions)

    eq = util.characteristic_eq(degree, associated)

    rts = roots(parse_expr(eq))
    nr_of_a = util.nr_of_alphas(rts)

    if len(rts) == 1:
        alphas = util.find_alphas_sol2(rts, init_conditions, nr_of_a)
        return util.build_solution2(rts, alphas)
    else:
        alphas = util.find_alphas_sol1(rts, init_conditions, nr_of_a)
        return util.build_solution1(rts, alphas)
