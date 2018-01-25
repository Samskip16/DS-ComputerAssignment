from sympy import roots, solve, Symbol

from sympy.parsing.sympy_parser import parse_expr

template_sol1 = 'a * r**n'
template_sol2 = '(a + b * n) * r**n'

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']


# Transform the given homogeneous recurrence relation to a closed formula.
def solve_eq(init_conditions, associated):
    degree = len(init_conditions)

    eq = character_eq(degree, associated)

    rts = roots(parse_expr(eq))

    if degree == 2 and len(rts) == 1:
        alphas = find_alphas(rts, init_conditions, template_sol2)
        return build_solution(template_sol2, rts, alphas)

    else:
        alphas = find_alphas(rts, init_conditions, template_sol1)
        return build_solution(template_sol1, rts, alphas)


# Build a characteristic equation using a given degree and recurrence parts
def character_eq(degree, associated):
    func = '(x**' + str(degree) + ')'

    power = degree - 1
    for key, value in sorted(associated.items()):
        func += flip_sign(parse_expr(value))

        if power > 1:
            func += '*x**' + str(power)
        elif power == 1:
            func += '*x'

        power -= 1

    return func


# Find the values of the alpha's which are in the standard form of the function.
def find_alphas(rts, init_conditions, template):
    func = fill_in_roots(template, rts)
    func += ' - result'

    alphas = {}

    i = 1
    for n, result in init_conditions.items():
        func_temp = fill_in_n(func, n, result)
        func_temp = fill_in_alphas(func_temp, alphas)

        char = get_char(i)
        solving = solve(parse_expr(func_temp), Symbol(char))[0]

        alphas[char] = solving

        i += 1

    return alphas


# Fill the value of n and the belonging result in a given function.
def fill_in_n(func, n, result):
    return func.replace('n', str(n)).replace('result', str(result))


def fill_in_alphas(func, alphas):
    for k, v in alphas.items():
        func = func.replace(str(k), bracketize(v))

    return func


def fill_in_roots(template, rts):
    func = ''

    i = 1
    for key, value in sorted(rts.items()):
        r = bracketize(key)
        func += template.replace('a', get_char(i)).replace('r', r) + ' + '

        i += 1

    return func[:-3]


def build_solution(template, rts, alphas):
    func = fill_in_roots(template, rts)
    func = fill_in_alphas(func, alphas)

    return func


def flip_sign(val):
    if val > 0:
        return '-' + str(val)
    else:
        return '+' + str(abs(val))


def get_char(i):
    return alphabet[(i - 1)]


def bracketize(val):
    return '(' + str(val) + ')'
