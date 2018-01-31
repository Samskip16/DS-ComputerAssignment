from sympy import solve, Symbol

from sympy.parsing.sympy_parser import parse_expr
from itertools import islice

template_sol1 = '(a) * (r)**n'
template_sol2 = '() * (r)**n'

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']


# Build a characteristic equation using a given degree and recurrence parts
def characteristic_eq(degree, associated):
    func = '(x**' + str(degree) + ')'

    power = degree - 1
    for x in range(1, degree + 1):

        if x in associated:
            val = associated[x]
            func += flip_sign(parse_expr(val))

            if power > 1:
                func += '*x**' + str(power)
            elif power == 1:
                func += '*x'

        power -= 1

    return func


def find_alphas_sol1(rts, init_conditions, nr_of_assoc, particular=None):
    func = fill_in_roots_sol1(rts)
    return find_alphas(func, init_conditions, nr_of_assoc, particular)


def find_alphas_sol2(rts, init_conditions, nr_of_assoc, particular=None):
    func = fill_in_roots_sol2(rts)
    return find_alphas(func, init_conditions, nr_of_assoc, particular)


# Find the values of the alpha's which are in the standard form of the function.
def find_alphas(func, init_conditions, nr_of_assoc, particular):
    func += ' - result'

    if particular:
        func += ' + ' + particular

    alphas = {}

    i = 1
    for n, result in take(nr_of_assoc, init_conditions.items()):
        func_temp = fill_in_n(func, n, result)
        func_temp = fill_in_values(func_temp, alphas)

        char = get_char(i)
        p = parse_expr(func_temp)
        solving = solve(parse_expr(func_temp), Symbol(char), dict=True)[0]

        alphas.update(solving)

        i += 1

    return alphas


# Fill the value of n and the belonging result in a given equation.
def fill_in_n(func, n, result):
    return func.replace('n', str(n)).replace('result', str(result))


# Fill values of the dictionary in a given equation.
def fill_in_values(func, values):
    for k, v in values.items():
        func = func.replace(str(k), bracketize(v))

    return func


# Fill the values of the known roots in a given template.
# When there are multiple roots the template gets automatically expanded.
def fill_in_roots_sol1(rts):
    func = ''

    i = 1
    for key, value in sorted(rts.items()):
        r = str(key)
        temp_template = ''

        if value > 1:
            for y in range(0, value+1):
                if y == 0:
                    temp_template += get_char(i)
                if y == 1:
                    temp_template += ' + ' + get_char(i+1) + '*n'
                if 1 < y < value:
                    temp_template += ' + ' + get_char(i+y)+'*n**' + str(y)
                if y == value:
                    func += template_sol1.replace('a', temp_template).replace('r', r) + ' + '
        else:
            func += template_sol1.replace('a', get_char(i)).replace('r', r) + ' + '

        i += 1

    return func[:-3]


def fill_in_roots_sol2(rts):
    func = ''

    rt = list(rts.items())[0]
    for i in range(1, rt[1] + 1):
        if i >= 2:
            func += get_char(i) + ' * (n**' + str(i - 1) + ') + '
        else:
            func += get_char(i) + ' + '

    func = bracketize(func[:-3])
    func = template_sol2.replace('()', func).replace('r', str(rt[0]))

    return func


# Build the final closed formula using the roots and alpha's
def build_solution1(rts, alphas):
    func = fill_in_roots_sol1(rts)
    func = fill_in_values(func, alphas)

    return func


def build_solution2(rts, alphas):
    func = fill_in_roots_sol2(rts)
    func = fill_in_values(func, alphas)

    return func


# Turn a positive value in to a negative one and vice versa.
def flip_sign(val):
    if val > 0:
        return '-' + str(val)
    else:
        return '+' + str(abs(val))


# Get the character of the alphabet belonging to the given index.
def get_char(i):
    return alphabet[(i - 1)]


def bracketize(val):
    return "(" + str(val) + ")"


def take(n, iterable):
    return list(islice(iterable, n))
