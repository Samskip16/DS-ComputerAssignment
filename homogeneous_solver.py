from sympy import roots, solve, Symbol, Number

from sympy.parsing.sympy_parser import parse_expr

template_sol1 = "alpha * r**n"
template_sol2 = "(alpha1 + alpha2 * n) + r**n"


def solve_eq(init_conditions, associated):
    # You have to implement this yourself!

    degree = len(init_conditions)

    func = "(x**" + str(degree) + ")"

    power = degree - 1
    for key, value in associated.items():
        func += plus_adder(parse_expr(value))

        if power > 1:
            func += "*x**" + str(power)
        elif power == 1:
            func += "*x"

        power -= 1

    rts = roots(parse_expr(func))

    print("Function: " + func)
    print(rts)

    if degree == 1:
        print("Function of degree 1")

        lel = ""
    elif degree == 2:
        print("Function of degree 2")

        if len(rts) == 1:
            rts_list = list(rts.values())

            a1 = solve_1st('a1', 0, init_conditions[0])
            print(a1)

            a2 = solve_1st('a2', 1, init_conditions[1], str(a1))
            print(a2)

            values = {"alpha1": a1, "alpha2": a2, "r": rts_list[0]}
            sol = fill_general_sol2(values)

            print("Solution: " + sol)
            return sol

        else:
            rts_dict = {}
            i = 1
            for key, value in rts.items():
                rts_dict["r" + str(i)] = key
                i += 1

            func = fill_roots(rts_dict)

            alphas = {}
            for n, result in init_conditions.items():
                func = fill_n(func, n, result, alphas)

                solving = solve(parse_expr(func))[0]

                if isinstance(solving, Number):
                    alphas["sol"] = solving
                else:
                    alphas.update(solving)

                lel2 = ""

    return ""


def fill_n(func, n, sol, alphas):
    for k, v in alphas.items():
        func = func.replace(str(k), str(v))

    return func.replace("n", str(n)) + " - " + str(sol)


def fill_roots(rts):
    sol = ""

    i = 1
    while i <= len(rts):
        r = rts[("r" + str(i))]
        sol += template_sol1.replace("alpha", ("alpha" + str(i))).replace("r", str(r)) + " + "

        i += 1

    return sol[:-3]


def fill_general_sol1(values, nr_of_alphas):
    sol = ""

    i = 0
    while i != nr_of_alphas:
        a = values[("alpha" + str(i))]
        r = values[("r" + str(i))]
        sol += template_sol1.replace("alpha", a).replace("r", r) + " + "

        i += 1

    return sol[:-3]


def fill_general_sol2(values):
    sol = template_sol2
    sol = sol.replace("alpha1", str(values["alpha1"]))
    sol = sol.replace("alpha2", str(values["alpha2"]))
    sol = sol.replace("r", str(values["r"]))

    return sol


def plus_adder(val):
    if val > 0:
        return "+" + str(val)
    else:
        return str(val)


def solve_1st(symbol, n, result, a1='a1'):
    s = Symbol(symbol)

    func = '(' + a1 + ' + a2 * ' + str(n) + ') * 2**' + str(n) + ' - ' + str(result)
    return solve(parse_expr(func), s)[0]
