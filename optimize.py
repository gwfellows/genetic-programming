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
        
def max_depth(exp, d=0):
    return max(map(lambda i: max_depth(i,d+1),exp)) if type(exp) in (tuple, list) else d
                    
def score(exp):
    fitness = 0
    for x in (i/10 for i in range(-10,10)):
        fitness += abs(
            interpreter.interpret(exp, {'X':x}) 
            - (goal(x)))
    return fitness+0.01*max_depth(exp)

FUNCTIONS = {add, mul,sub}
TERMINALS = {1.0,'X'}

import random
def my_shuffle(array):
    random.shuffle(array)
    return array

def test_crossover():        
    for crossover_rate in my_shuffle(list(_/10 for _ in range(1,10+1))*10):
        start = datetime.now()
        solution = interpreter.evolve(
                functions=FUNCTIONS,
                terminals=TERMINALS,
                fitness_function = lambda exp: score(exp),
                pop_size=3000,
                init_max_depth=5,
                crossover_rate=crossover_rate,
                selection_cutoff=0.5,
                verbose=False)
        end = datetime.now()
        print(crossover_rate,",",end.timestamp()-start.timestamp())

def test_pop_size():        
    for pop_size in my_shuffle(list(range(100,5000,100))*10):
        start = datetime.now()
        solution = interpreter.evolve(
                functions=FUNCTIONS,
                terminals=TERMINALS,
                fitness_function = lambda exp: score(exp),
                pop_size=pop_size,
                init_max_depth=5,
                crossover_rate=0.9,
                selection_cutoff=0.5,
                verbose=False)
        end = datetime.now()
        print(pop_size,",",end.timestamp()-start.timestamp())

test_pop_size();