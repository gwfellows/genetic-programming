import interpreter
import math
from datetime import datetime

def add(a, b):
    return a+b;

def sub(a, b):
    return a-b;

def mul(a, b):
    return a*b;

def exp(a,b):
    a, b = float(a), float(b)
    if a<=0:
        return 0
    return a**b;

goal = lambda x: x**5+x**3+x**2+x+1
        
def score(exp):
    fitness = 0
    for x in (i/10 for i in range(-10,10)):
        fitness += abs(
            interpreter.interpret(exp, {'X':x}) 
            - (goal(x)))
    return fitness

FUNCTIONS = {add, mul,sub,exp}
TERMINALS = {1.0,'X'}

import random
def my_shuffle(array):
    random.shuffle(array)
    return array
        
for crossover_rate in my_shuffle(list(_/10 for _ in range(7,10+1))*10):
    start = datetime.now()
    solution = interpreter.evolve(
            functions=FUNCTIONS,
            terminals=TERMINALS,
            fitness_function = lambda exp: score(exp),
            pop_size=188,
            init_max_depth=10,
            crossover_rate=crossover_rate,
            selection_cutoff=0.5,
            verbose=True)
    end = datetime.now()
    print(crossover_rate,",",end.timestamp()-start.timestamp())