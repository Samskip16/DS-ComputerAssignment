from sympy import solve, Symbol

from sympy.parsing.sympy_parser import parse_expr

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


# Find the values of the alpha's which are in the standard form of the function.
def find_alphas(rts, init_conditions, template, particular=None):
    func = fill_in_roots(template, rts)
    func += ' - result'

    if particular:
        func += ' + ' + particular

    alphas = {}

    i = 1
    for n, result in init_conditions.items():
        func_temp = fill_in_n(func, n, result)
        func_temp = fill_in_alphas(func_temp, alphas)

        char = get_char(i)
        p = parse_expr(func_temp)
        solving = solve(parse_expr(func_temp), Symbol(char))[0]

        alphas[char] = solving

        i += 1

    return alphas


# Fill the value of n and the belonging result in a given equation.
def fill_in_n(func, n, result):
    return func.replace('n', str(n)).replace('result', str(result))


# Fill the values of the known alpha's in a given equation.
def fill_in_alphas(func, alphas):
    for k, v in alphas.items():
        func = func.replace(str(k), bracketize(v))

    return func


# Fill the values of the known roots in a given template.
# When there are multiple roots the template gets automatically expanded.
def fill_in_roots(template, rts):
    func = ''

    i = 1
    for key, value in sorted(rts.items()):
        r = str(key)
        func += template.replace('a', get_char(i)).replace('r', r) + ' + '

        i += 1

    return func[:-3]


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
