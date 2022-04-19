import interpreter
import math

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
        
        goal = lambda x: x**4+x**3+x**2+x+1
        
        def score(exp):
            fitness = 0
            for x in (i/10 for i in range(-10,10)):
                fitness += abs(
                    interpreter.interpret(exp, {'X':x}) 
                    - (goal(x)))
            return fitness
        
        FUNCTIONS = {add, mul,sub,exp}
        TERMINALS = {1,10,5,'X'}
        
        solution = interpreter.evolve(
            functions=FUNCTIONS,
            terminals=TERMINALS,
            fitness_function = lambda exp: score(exp),
            pop_size=3000,
            init_max_depth=10,
            crossover_rate=0.8)
        
        x1=[]
        y1=[]
        x2=[]
        y2=[]
        
        
        for x in (i/10 for i in range(-10,10)):
            x1.append(x)
            y1.append(goal(x))
        
        for x in (i/10 for i in range(-10,10)):
            x2.append(x)
            y2.append(interpreter.interpret(solution, {'X':x}))

        
        import matplotlib.pyplot as plt
        plt.scatter(x1,y1, color='blue',marker='o')
        plt.plot(x2,y2, color='red', linestyle='--')
        plt.show()

        
        #print("PI = ", interpreter.interpret(solution))
        interpreter.graphprint(solution, "sol.gv")
        interpreter.asciiprint(solution)
    

if __name__ == '__main__':
    unittest.main()
