import interpreter
import math
from inspect import signature
import argparse
import os
import sys
import math
import statistics
import csv

import matplotlib.pyplot as plt

my_parser = argparse.ArgumentParser(
    prog="symreg", description="Use symbolic regression to fit a curve to data"
)
my_parser.add_argument(
    "Path", metavar="path", type=str, help="the path to the data (csv format)"
)

my_parser.add_argument(
    "--suggest",
    action="store",
    choices=["linear", "exponential", "quadratic", "poly3", "poly4", "log"],
    required=False,
    help="suggest a class of functions as the starting point for evolution",
)

my_parser.add_argument(
    "--psize",
    action="store",
    type=int,
    required=False,
    help="the population size to use (30 by default)",
)

my_parser.add_argument(
    "--updatefreq",
    action="store",
    type=int,
    required=False,
    help="how often to update the display (every 10 generations by default)",
)

my_parser.add_argument(
    "--sizepenalty",
    action="store",
    type=float,
    required=False,
    help="how much to penalize large trees (0.001 by default)",
)

args = my_parser.parse_args()


def add(a, b):
    ret = a + b
    if math.isnan(ret) or math.isinf(ret):
        return 0
    return ret


def sub(a, b):
    return a - b


def mul(a, b):
    ret = a * b
    if math.isnan(ret) or math.isinf(ret):
        return 0
    return a * b


def div(a, b):
    if b == 0:
        return 0
    ret = a / b
    if math.isnan(ret) or math.isinf(ret):
        return 0
    return a / b


def sqrt(a):
    if a < 0:
        return 0
    return math.sqrt(a)


def power(a, b):
    a, b = float(a), float(b)
    if a <= 0:
        return 0
    ret = a**b
    if math.isnan(ret) or math.isinf(ret):
        return 0
    return ret


def squared(a):
    return power(a, 2)


def ln(a):
    if a <= 0:
        return -1000000
    return math.log(a)


def log(a, b):
    if (a <= 0) or (b <= 1):
        return -1000000
    return math.log(a, b)


def cos(a):
    try:
        return math.cos(a)
    except:
        return 0


# print a tree as a expression
# only works with binary operators +, *, / and -
# and cosine, and the constant pi
def expr_print(exp):
    if type(exp) in (str, int, float):
        if exp == math.pi:
            return "pi"
        return str(exp)
    if exp[0] == add:
        return "(" + expr_print(exp[1]) + "+" + expr_print(exp[2]) + ")"
    if exp[0] == mul:
        return "(" + expr_print(exp[1]) + "*" + expr_print(exp[2]) + ")"
    if exp[0] == sub:
        return "(" + expr_print(exp[1]) + "-" + expr_print(exp[2]) + ")"
    if exp[0] == div:
        return "(" + expr_print(exp[1]) + "/" + expr_print(exp[2]) + ")"
    if exp[0] == power:
        return "(" + expr_print(exp[1]) + "**(" + expr_print(exp[2]) + "))"
    if exp[0] == cos:
        return "cos(" + expr_print(exp[1]) + ")"
    if exp[0] == log:
        return "log(" + expr_print(exp[1]) + " , " + expr_print(exp[2]) + ")"
    if exp[0] == ln:
        return "ln(" + expr_print(exp[1]) + ")"
    if exp[0] == squared:
        return "(" + expr_print(exp[1]) + "**(2))"


data = []
# log10 transistors-per-microprocessor
with open(args.Path, mode="r") as d:
    reader = csv.reader(d)
    data = [(float(rows[0]), float(rows[1])) for rows in reader]


def get_differences(data):
    diffs = []
    for i in range(1, len(data)):
        x = data[i][0]
        y = (data[i][1] - data[i - 1][1]) / (data[i][0] - data[i - 1][0])
        diffs.append([x, y])
    return diffs


# use NRMSE
data_diffs = get_differences(data)
data_diffs_mean = statistics.mean(row[1] for row in data_diffs)


def n_nodes(exp, d=0):
    return sum(map(n_nodes, exp)) if type(exp) in (tuple, list) else 1


if args.sizepenalty:
    sizepenalty = args.sizepenalty
else:
    sizepenalty = 0.001

# n=0


def score(exp):
    global n
    square_errors = []

    data_to_score = [
        [pair[0], interpreter.interpret(exp, {"X": pair[0]})] for pair in data
    ]
    diffs_to_score = get_differences(data_to_score)

    try:
        for i, pair in enumerate(diffs_to_score):
            square_errors.append((diffs_to_score[i][1] - data_diffs[i][1]) ** 2)
    except OverflowError:
        print("overflow")
        return float("inf")
    # import matplotlib.pyplot as plt

    # plt.plot([i for i in range(0,36)], [interpreter.interpret(exp, {'X':i}) for i in range(0,36)])
    """if random.random()<0.05:
        print(expr_print(exp)+"\n"+str(math.sqrt(statistics.mean(square_errors))/abs(data_diffs_mean) + sizepenalty*n_nodes(exp)))"""
    # plt.show()
    # plt.savefig("GRPH"+str(n)+".png")
    # plt.clf()
    # plt.title("")

    # n+=1

    return math.sqrt(statistics.mean(square_errors)) / abs(
        data_diffs_mean
    ) + sizepenalty * n_nodes(exp)


import random


def randnum():
    return random.random() * 4 - 2


def nargs(func):
    return len(signature(func).parameters)


def _handle(t):
    return t() if callable(t) else t


def randexp(F, T, maxdepth=5):
    U = list(F.union(T))

    def _randexp(atom, depth=2):
        if atom in T:
            return _handle(atom)
        if atom in F:
            return (
                atom,
                *[
                    _randexp(
                        random.choice(U)
                        if depth < maxdepth
                        else random.choice(list(T)),
                        depth + 1,
                    )
                    for _ in range(nargs(atom))
                ],
            )

    return _randexp(random.choice(list(F)))


def lnfunc():
    return [
        log,
        [add, "X", randexp(FUNCTIONS, TERMINALS, 3)],
        randexp(FUNCTIONS, TERMINALS, 3),
    ]


def powerfunc():
    return [
        mul,
        [power, randexp(FUNCTIONS, TERMINALS, 2), "X"],
        randexp(FUNCTIONS, TERMINALS, 2),
    ]


def linearfunc():
    return [mul, randexp(FUNCTIONS, TERMINALS, 3), "X"]


def poly2func():
    return [add, linearfunc(), [mul, randexp(FUNCTIONS, TERMINALS, 3), [mul, "X", "X"]]]


def poly3func():
    return [
        add,
        poly2func(),
        [mul, randexp(FUNCTIONS, TERMINALS, 3), [mul, [mul, "X", "X"], "X"]],
    ]


def poly4func():
    return [
        add,
        poly3func(),
        [
            mul,
            randexp(FUNCTIONS, TERMINALS, 3),
            [mul, [mul, [mul, "X", "X"], "X"], "X"],
        ],
    ]


# evolve vectors for function types

if args.suggest:
    templates = (
        (
            1,
            {
                "linear": linearfunc,
                "exponential": powerfunc,
                "quadratic": poly2func,
                "poly3": poly3func,
                "poly4": poly4func,
                "log": lnfunc,
            }[args.suggest],
        ),
    )
    FUNCTIONS = {add, mul, sub}
    TERMINALS = {randnum, 1}
else:
    templates = ((1, "RANDOM"),)
    FUNCTIONS = {add, mul, sub, ln}
    TERMINALS = {randnum, 1, "X"}

if args.psize:
    psize = args.psize
else:
    psize = 30

if args.updatefreq:
    updatefreq = args.updatefreq
else:
    updatefreq = 10


solution = interpreter.evolve(
    functions=FUNCTIONS,
    terminals=TERMINALS,
    fitness_function=lambda exp: score(exp),
    pop_size=psize,
    init_max_depth=3,
    crossover_rate=0.8,
    selection_cutoff=0.1,
    mutation_rate=0.1,
    verbose=True,
    updatefreq=updatefreq,
    templates=templates,
)

print("---")

# use NRMSE
data_mean = statistics.mean(row[1] for row in data)


def nscore(exp):
    square_errors = []

    data_to_score = [
        [pair[0], interpreter.interpret(exp, {"X": pair[0]})] for pair in data
    ]
    try:
        for i, pair in enumerate(data_to_score):
            square_errors.append((data_to_score[i][1] - data[i][1]) ** 2)
    except OverflowError:
        return float("inf")

    return math.sqrt(statistics.mean(square_errors)) / abs(data_mean) + 0.01 * n_nodes(
        exp
    )


os.system("cls")
os.system("clear")

print("matching vertical shift...")

C = interpreter.evolve(
    functions={add, mul, sub, div, power},
    terminals={randnum, 1},
    fitness_function=lambda exp: nscore([add, exp, solution]),
    pop_size=20,
    init_max_depth=3,
    crossover_rate=0.8,
    selection_cutoff=0.0,
    gens_cutoff=200,
    mutation_rate=0.1,
    verbose=False,
    templates=((1, "RANDOM"),),
)

os.system("cls")

x1 = []
y1 = []
x2 = []
y2 = []


for pair in data:
    x1.append(pair[0])
    y1.append(pair[1])

mx = max(pair[0] for pair in data)
mn = min(pair[0] for pair in data)

for x in range(0, 1000):
    x = (x / 1000) * (mx - mn) + mn
    x2.append(x)
    y2.append(interpreter.interpret([add, solution, C], {"X": x}))


plt.scatter(x1, y1, color="blue", marker="o")
plt.plot(x2, y2, color="red", linestyle="--")
plt.show()


"""
interpreter.graphprint([add,solution,C], "sol.gv")
print()
print(expr_print([add,solution,C]))
print()
print()
print(expr_print(interpreter.simplify([add,solution,C])))
print()"""

print("found model f(X) = ")
from sympy import latex, sympify

print(
    latex(
        sympify(expr_print(interpreter.simplify([add, solution, C])))
        .expand()
        .simplify()
    ).replace("log", "ln")
)
print()
