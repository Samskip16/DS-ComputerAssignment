from sympy import roots, solve, Symbol, simplify

from sympy.parsing.sympy_parser import parse_expr

import util


# Transform the given homogeneous recurrence relation to a closed formula.
def solve_eq(init_conditions, associated, f_n_list):
    degree = len(init_conditions)

    eq = util.characteristic_eq(degree, associated)

    rts = roots(parse_expr(eq))

    particular = find_part_sol(rts, associated)

    if len(rts) == 1:
        alphas = util.find_alphas_sol2(rts, init_conditions)
        return build_solution2(rts, alphas, particular)
    else:
        alphas = util.find_alphas_sol1(rts, init_conditions)
        return build_solution1(rts, alphas, particular)


def find_part_sol(rts, associated):
    bs = {}

    s = int(input("S:"))
    t = int(input("T:"))

    nr_of_bs = input('Nr of B: ')
    for i in range(int(nr_of_bs)):
        bs[i] = input('B' + str(i) + ': ')

    form = build_particular_form(s, t, bs, rts)
    filled = fill_particular(form, associated)

    solving = solve(parse_expr(filled), Symbol(get_char(1)))[0]
    return form.replace(get_char(1), bracketize(solving))


def build_particular_form(s, t, bs, rts):
    func = ''
    if s in rts:
        func += 'n**' + rts[s]

    func += '('

    for i in range(len(bs)):
        if t > 1:
            func += get_char(i + 1) + '*' + bracketize('n**' + str(t)) + ' + '
        elif t == 1:
            func += get_char(i + 1) + '*n + '
        else:
            func += get_char(i + 1) + ' + '

        t -= 1

    func = func[:-3] + ')'
    func += ' * ' + bracketize(s) + '**n'

    return func


def fill_particular(form, associated):
    filled = ''

    for k, v in associated.items():
        m = parse_expr(v)

        adjusted_form = form.replace('**n', '**n-' + str(k))
        filled += str(m) + ' * ' + bracketize(adjusted_form) + ' '

    filled += '-' + bracketize(form)
    return filled


# Build the final closed formula using the roots and alpha's
def build_solution1(rts, alphas, particular):
    return util.build_solution1(rts, alphas) + particular


def build_solution2(rts, alphas, particular):
    return util.build_solution2(rts, alphas) + particular


# Get the character of the alphabet belonging to the given index.
def get_char(i):
    return util.get_char(i)


def bracketize(val):
    return util.bracketize(val)
