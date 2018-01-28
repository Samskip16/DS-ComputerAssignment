from sympy import roots

from sympy.parsing.sympy_parser import parse_expr

import util

template_sol1 = '(a) * (r)**n'
template_sol2 = '((a) + (b) * n) * (r)**n'


# Transform the given homogeneous recurrence relation to a closed formula.
def solve_eq(init_conditions, associated):
    degree = len(init_conditions)

    eq = util.character_eq(degree, associated)

    rts = roots(parse_expr(eq))

    if degree == 2 and len(rts) == 1:
        alphas = util.find_alphas(rts, init_conditions, template_sol2)
        return build_solution(template_sol2, rts, alphas)

    else:
        alphas = util.find_alphas(rts, init_conditions, template_sol1)
        return build_solution(template_sol1, rts, alphas)


# Build the final closed formula using the roots and alpha's
def build_solution(template, rts, alphas):
    func = util.fill_in_roots(template, rts)
    func = util.fill_in_alphas(func, alphas)

    return func
