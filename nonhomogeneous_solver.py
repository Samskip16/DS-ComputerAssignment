from sympy import roots, solve, Symbol

from sympy.parsing.sympy_parser import parse_expr

import util


# Transform the given homogeneous recurrence relation to a closed formula.
def solve_eq(init_conditions, associated, f_n_list):
    degree = len(init_conditions)

    eq = util.characteristic_eq(degree, associated)

    rts = roots(parse_expr(eq))

    particular = find_part_sol(rts, associated, f_n_list[0])

    if len(rts) == 1:
        alphas = util.find_alphas_sol2(rts, init_conditions, len(associated), particular)
        return build_solution2(rts, alphas, particular)
    else:
        alphas = util.find_alphas_sol1(rts, init_conditions, len(associated), particular)
        return build_solution1(rts, alphas, particular)


def find_part_sol(rts, associated, f_n):
    t = find_t(f_n)
    s = find_s(f_n)

    form = build_particular_form(s, t, rts)
    filled = fill_particular(form, associated, f_n)

    ps = []
    for i in range(1, t + 2):
        ps.append(Symbol(get_char(i)))

    solving = solve(parse_expr(filled), ps, dict=True)[0]

    return util.fill_in_values(form, solving)


def build_particular_form(s, t, rts):
    func = ''
    if s in rts:
        func += 'n**' + str(rts[s])

    func += '('

    for i in range(t + 1):
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


def fill_particular(form, associated, f_n):
    filled = ''

    for k, v in associated.items():
        m = str(parse_expr(v))

        if m[:1] != '-':
            m = '+' + m

        adjusted_form = form.replace('**n', '**(n-' + str(k) + ')')
        filled += m + ' * ' + adjusted_form + ' '

    filled += ' + ' + f_n
    filled += ' - ' + bracketize(form)

    return filled


def find_s(f_n):
    i = j = f_n.find('**n')

    print('i:', f_n[i])
    print('j-1:', f_n[j - 1])

    if i == -1:
        return 1

    while f_n[j - 1].isdigit():
        j -= 1

    if f_n[j - 1] == ')':
        while f_n[j - 1] != '(':
            j -= 1

        i -= 1

    return int(f_n[j:i])


def find_t(f_n):
    i = f_n.find('n**')

    if i == -1:
        return 0

    j = i + 3
    while j < len(f_n) and f_n[j].isdigit():
        j += 1

    return int(f_n[i + 3:j])


# Build the final closed formula using the roots and alpha's
def build_solution1(rts, alphas, particular):
    return util.build_solution1(rts, alphas) + ' + ' + particular


def build_solution2(rts, alphas, particular):
    return util.build_solution2(rts, alphas) + ' + ' + particular


# Get the character of the alphabet belonging to the given index.
def get_char(i):
    return util.get_char(i)


def bracketize(val):
    return util.bracketize(val)
