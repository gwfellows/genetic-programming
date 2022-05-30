import interpreter
import math
from inspect import signature
import argparse
import os
import sys
import math
import matplotlib.pyplot as plt            
import statistics
import csv

my_parser = argparse.ArgumentParser(prog='symreg',description='Use symbolic regression to fit a curve to data')
my_parser.add_argument('Path',
                       metavar='path',
                       type=str,
                       help='the path to the data (csv format)')
                       
my_parser.add_argument('--suggest',
                        action='store',
                        choices=['linear','exponential','quadratic','poly3','poly4','log'],
                        required=False,
                        help='suggest a class of functions as the starting point for evolution')

args = my_parser.parse_args()

def add(a, b):
    ret = a+b
    if math.isnan(ret) or math.isinf(ret):
        return 0
    return ret;

def sub(a, b):
    return a-b;

def mul(a, b):
    ret = a*b
    if math.isnan(ret) or math.isinf(ret):
        return 0
    return a*b;

def div(a, b):
    if b==0:
        return 0
    ret = a/b
    if math.isnan(ret) or math.isinf(ret):
        return 0
    return a/b

def sqrt(a):
    if a<0:
        return 0
    return math.sqrt(a)

def power(a,b):
    a, b = float(a), float(b)
    if a<=0:
        return 0
    ret = a**b
    if math.isnan(ret) or math.isinf(ret):
        return 0
    return ret

def squared(a):
    return power(a,2)

def ln(a):
    if a<=0:
        return 0
    return math.log(a)

def log(a, b):
    if (a<=0) or (b<=1):
        return -1000000
    return math.log(a, b)

def cos(a):
    try:
        return math.cos(a)
    except:
        return 0

data = []
#log10 transistors-per-microprocessor
with open(args.Path, mode='r') as d:
    reader = csv.reader(d)
    data = [(float(rows[0]),float(rows[1])) for rows in reader]

def get_differences(data):
    diffs = []
    for i in range(1,len(data)):
        x = data[i][0]
        y = (data[i][1]-data[i-1][1])/(data[i][0]-data[i-1][0])
        diffs.append([x,y])
    return diffs
    
#use NRMSE
data_diffs = get_differences(data)
data_diffs_mean = statistics.mean(row[1] for row in data_diffs)

def n_nodes(exp, d=0):
    return sum(map(n_nodes,exp)) if type(exp) in (tuple, list) else 1

def score(exp):
    square_errors = []
   
    data_to_score = [[pair[0],interpreter.interpret(exp, {'X':pair[0]})] for pair in data]
    diffs_to_score = get_differences(data_to_score)
    
    try:
        for i, pair in enumerate(diffs_to_score):
            square_errors.append((diffs_to_score[i][1]-data_diffs[i][1])**2)
    except OverflowError:
        print("overflow")
        return float("inf")
        
    return math.sqrt(statistics.mean(square_errors))/abs(data_diffs_mean) + 0.001*n_nodes(exp)

import random

def randnum():
    return random.random()*4-2

#print a tree as a expression
#only works with binary operators +, *, / and -
#and cosine, and the constant pi
def expr_print(exp):
    if type(exp) in (str, int, float):
        if exp == math.pi:
            return "pi"
        return str(exp)
    if exp[0] == add:
        return "("+expr_print(exp[1])+"+"+expr_print(exp[2])+")"
    if exp[0] == mul:
        return "("+expr_print(exp[1])+"*"+expr_print(exp[2])+")"
    if exp[0] == sub:
        return "("+expr_print(exp[1])+"-"+expr_print(exp[2])+")"
    if exp[0] == div:
        return "("+expr_print(exp[1])+"/"+expr_print(exp[2])+")"
    if exp[0] == power:
        return "("+expr_print(exp[1])+"**("+expr_print(exp[2])+"))"
    if exp[0] == cos:
        return "cos("+expr_print(exp[1])+")"
    if exp[0] == log:
        return "log("+expr_print(exp[1])+" , "+expr_print(exp[2])+")"
    if exp[0] == ln:
        return "ln("+expr_print(exp[1])+")"
    if exp[0] == squared:
        return "("+expr_print(exp[1])+"**(2))"
        
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
            return (atom, *[_randexp(
                random.choice(U) if depth<maxdepth else random.choice(list(T)), depth+1
                ) for _ in range(nargs(atom))])
    return _randexp(random.choice(list(F)))


def lnfunc():
    return [log, [add, 'X', randexp(FUNCTIONS,TERMINALS,3)], randexp(FUNCTIONS,TERMINALS,3)]

def powerfunc():
    return [mul, [power, randexp(FUNCTIONS,TERMINALS,2), 'X'], randexp(FUNCTIONS,TERMINALS,2)]

def linearfunc():
    return [mul, randexp(FUNCTIONS,TERMINALS,3), 'X']

def poly2func():
    return [add, linearfunc(), [mul, randexp(FUNCTIONS,TERMINALS,3), [mul, 'X', 'X']]]

def poly3func():
    return [add, poly2func(), [mul, randexp(FUNCTIONS,TERMINALS,3), [mul, [mul, 'X', 'X'],'X']]]

def poly4func():
    return [add, poly3func(), [mul, randexp(FUNCTIONS,TERMINALS,3), [mul, [mul, [mul, 'X', 'X'],'X'],'X']]]

#evolve vectors for function types

if args.suggest:
    templates = ((1, {'linear':linearfunc,
                'exponential':powerfunc,
                'quadratic':poly2func,
                'poly3':poly3func,
                'poly4':poly4func,
                'log':lnfunc}[args.suggest]),)
    FUNCTIONS = {add,mul,sub}
    TERMINALS = {randnum,1}
else:
    templates = ((1, 'RANDOM'),)
    FUNCTIONS = {add,mul,sub,div,ln}
    TERMINALS = {randnum,1,'X'}

solution = interpreter.evolve(
    functions=FUNCTIONS,
    terminals=TERMINALS,
    fitness_function = lambda exp: score(exp),
    pop_size=30,
    init_max_depth=3,
    crossover_rate=0.8,
    selection_cutoff=0.1,
    mutation_rate=0.1,
    verbose=True,
    templates = templates
    )

print("---")

#use NRMSE
data_mean = statistics.mean(row[1] for row in data)

def nscore(exp):
    square_errors = []
    
    data_to_score = [[pair[0],interpreter.interpret(exp, {'X':pair[0]})] for pair in data]
    try:
        for i, pair in enumerate(data_to_score):
            square_errors.append((data_to_score[i][1]-data[i][1])**2)
    except OverflowError:
        return float('inf')
        
    return math.sqrt(statistics.mean(square_errors))/abs(data_mean) + 0.01*n_nodes(exp)
    
os.system("cls")
print("matching vertical shift...")

C = interpreter.evolve(
    functions={add,mul,sub,div,power},
    terminals={randnum,1},
    fitness_function = lambda exp: nscore([add,exp,solution]),
    pop_size=20,
    init_max_depth=3,
    crossover_rate=0.8,
    selection_cutoff=0.0,
    gens_cutoff=200,
    mutation_rate=0.1,
    verbose=False,
    templates = ((1, 'RANDOM'),)
    )

os.system("cls")

x1=[]
y1=[]
x2=[]
y2=[]


for pair in data:
    x1.append(pair[0])
    y1.append(pair[1])

mx = max(pair[0] for pair in data)
mn = min(pair[0] for pair in data)

for x in range(0,1000):
    x = (x/1000)*(mx-mn) + mn
    x2.append(x)
    y2.append(interpreter.interpret([add,solution,C], {'X':x}))


plt.scatter(x1,y1, color='blue',marker='o')
plt.plot(x2,y2, color='red', linestyle='--')
#plt.yscale('log')
plt.show()


#print("PI = ", interpreter.interpret(solution))
#print(max_depth(solution))
'''
interpreter.graphprint([add,solution,C], "sol.gv")
print()
print(expr_print([add,solution,C]))
print()
print()
print(expr_print(interpreter.simplify([add,solution,C])))
print()'''

print("found model f(X) = ")
from sympy import latex, sympify
print(latex(sympify(expr_print(interpreter.simplify([add,solution,C]))).expand().simplify()).replace("log","ln"))
print()

#- 0.013858710635380252 X^{4} + 0.53697500977103116 X^{3} - 6.5551372986654139 X^{2} + 28.389679800710066 X - 16.376144862352344

#0.3371227270112964 X + 11.10095240393376 \log{\left(X + 1.9038478537754524 \right)} + 42.95437418392193
#- 0.015400722326537062 X^{4} + 0.58683298779939933 X^{3} - 7.1004068081623992 X^{2} + 30.830328731161897 X - 20.806366953841057
#logistic curves
'''
X \left(0.00067151805666508732 X^{5} - 0.032360861953569867 X^{4} + 0.58098621326037945 X^{3} - 4.6483746456198377 X^{2} + 15.03502728428022 X - 9.3563119247896713\right)'''