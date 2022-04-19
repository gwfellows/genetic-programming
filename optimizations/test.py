from __future__ import print_function

import interpreter
import math

from sys import getsizeof, stderr
from itertools import chain
from collections import deque
try:
    from reprlib import repr
except ImportError:
    pass


def add(a, b):
    return a+b;

def sub(a, b):
    return a-b;

def mul(a, b):
    return a*b;

def div(a, b):
    if b==0:
        return 0
    return a/b

def sqrt(a):
    if a<0:
        return 0
    return math.sqrt(a)

def exp(a,b):
    a, b = float(a), float(b)
    if a<=0:
        return 0
    return a**b;

def ln(a):
    if a<=0:
        return 0
    return math.log(a)
'''
https://code.activestate.com/recipes/577504/
'''

def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)


##### Example call #####

import unittest

class Test(unittest.TestCase):
    '''
    def test_interpret(self):
        self.assertEqual(
            interpreter.interpret(
                (div, (sub, (exp, 'X', 'Y'), 10), 3),
                {'X':5, 'Y':10}),
            ((5**10)-10)/3
            )
        self.assertEqual(
            interpreter.interpret(
                (add, (mul, 'X', 2), 10),
                {'X':5}),
            (5*2)+10
            )
        self.assertEqual(
            interpreter.interpret(
                (div, 10, 0)),
            0
            )
        self.assertEqual(
            interpreter.interpret(
                (add, (mul, 'X', 2), 10),
                {'X':-100}),
            (-100*2)+10
            )

    def test_asciiprint(self):
        self.assertEqual(
            interpreter.asciiprint(
                (add, (sub, 'X', 100), (sqrt, 'Y'))
                 ),
                "add\n|sub\n||X\n||100\n|sqrt\n||Y"
            )
                

    def test_randexp(self):
        FUNCTIONS = {add, sub, mul, div, sqrt, exp, ln}
        TERMINALS = {0,1,2,3,4,5, 'X', 'Y'}
        
        #just making sure there are no errors
        for _ in range(1000):
            interpreter.interpret(
                interpreter.randexp(FUNCTIONS, TERMINALS),
                {'X':5, 'Y':10}
                )
    
        interpreter.graphprint(interpreter.randexp(FUNCTIONS, TERMINALS, 100))
        
    def test_get_subindices(self):
        FUNCTIONS = {add, sub, mul, div, sqrt, exp, ln}
        TERMINALS = {0,1,2,3,4,5, 'X', 'Y'}
        
        self.assertEqual(
            interpreter.get_subindices([add, [ln, 2], [mul, 2, 3]]),
            [(1,), (1, 1), (2,), (2, 2), (2, 1)]
        )
        
        #just making sure there are no errors
        for _ in range(1000):
            interpreter.get_subindices(
                interpreter.randexp(FUNCTIONS, TERMINALS)
                )
                
    def test_crossover(self):
        FUNCTIONS = {add, sub, mul, div, sqrt, exp, ln}
        TERMINALS = {0,1,2,3, 'X', 'Y'}
        
        a = interpreter.randexp(FUNCTIONS, TERMINALS, 20)
        b = interpreter.randexp(FUNCTIONS, TERMINALS, 20)
        
        interpreter.graphprint(a, "A1.gv")
        interpreter.graphprint(b, "B1.gv")
        
        a, b = interpreter.crossover(a,b)
        
        interpreter.graphprint(a, "A2.gv")
        interpreter.graphprint(b, "B2.gv")
    '''
    
        
    def test_evolve(self):
        import math
        
        def score_symbolic_regression(exp):
            fitness = 0
            for x in (i/20 for i in range(-20,20)):
                fitness += abs(
                    interpreter.interpret(exp, {'X':x}) 
                    - (x**4+x**3+x**2+x+1))
            return (fitness + 0.000001*total_size(exp)) if fitness<=0.99 else fitness
        
        FUNCTIONS = {add, mul, div}
        TERMINALS = {-2.0,-1.0,0.0,1.0,2.0, 'X'}
        
        #print("PI = ", interpreter.interpret(solution))
        #interpreter.graphprint(solution, "sol.gv")
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots()
        
        pop_sizes = list(_/50 for _ in range(25,51))
        avggens = [0]*len(pop_sizes)
        for i, pop_size in enumerate(pop_sizes):
            print(pop_size, avggens)
            for _ in range(10):
                print(" "+str(_))
                xs, ys = interpreter.evolve(
                    functions=FUNCTIONS,
                    terminals=TERMINALS,
                    fitness_function = score_symbolic_regression,
                    pop_size=188,
                    init_max_depth=5,
                    crossover_rate=0.9)
                avggens[i] += max(xs)/10
        
        ax.plot(pop_sizes, avggens, color='blue')

        print(avggens)
            
        ax.set(xlabel='Crossover Rate', ylabel='Individuals Proccessed to Reach Completion (Avg. of 1000)')
        ax.grid()
        fig.savefig("test.png")
        plt.show()
    

if __name__ == '__main__':
    unittest.main()
