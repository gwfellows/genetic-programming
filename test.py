import interpreter
import math

#damped oscillator
#adjust timeline

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

def cos(a):
    try:
        return math.cos(a)
    except:
        return 0
        
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
        import matplotlib.pyplot as plt            
        
        #goal = lambda x: x**5+x**3+x**2+x+1
        goal = lambda x: math.sin(x*math.pi)
        #goal = lambda x: x%1
        #goal = lambda x: math.log(x+1.1)
        
        import csv

        data = []
        
        with open('data.csv', mode='r') as d:
            reader = csv.reader(d)
            data = [(float(rows[0]),float(rows[1])) for rows in reader]

        def n_nodes(exp, d=0):
            return sum(map(n_nodes,exp)) if type(exp) in (tuple, list) else 1
        
        #r = range(-10,10,1)
        
        '''def score(exp):
            fitness = 0
            for x in (i/10 for i in r):
                fitness += abs(
                    interpreter.interpret(exp, {'X':x}) 
                    - (goal(x)))
            return fitness+0.01*max_depth(exp)'''
        
        def score(exp):
            fitness = 0
            for pair in data:
                x = pair[0]
                y = pair[1]
                fitness += abs(interpreter.interpret(exp, {'X':x}) - y)
            return fitness+0.01*n_nodes(exp)
        
        import random
        
        def randnum():
            return random.random()*2-1
            
        FUNCTIONS = {add, mul}
        TERMINALS = {randnum,'X'}
        
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
            if exp[0] == cos:
                return "cos("+expr_print(exp[1])+")"
        
        
        solution = interpreter.evolve(
            functions=FUNCTIONS,
            terminals=TERMINALS,
            fitness_function = lambda exp: score(exp),
            pop_size=300,
            init_max_depth=4,
            crossover_rate=0.9,
            selection_cutoff=2,
            verbose=True)
        
        x1=[]
        y1=[]
        x2=[]
        y2=[]
        
        
        for pair in data:
            x1.append(pair[0])
            y1.append(pair[1])
        
        for x in range(0,5000):
            x2.append(x)
            y2.append(interpreter.interpret(solution, {'X':x}))

        
        plt.scatter(x1,y1, color='blue',marker='o')
        plt.plot(x2,y2, color='red', linestyle='--')
        
        plt.show()

        
        #print("PI = ", interpreter.interpret(solution))
        #print(max_depth(solution))
        interpreter.graphprint(solution, "sol.gv")
        print()
        print(expr_print(solution))
        print()
        from sympy import sympify
        print(sympify(expr_print(solution)).expand().simplify())
        interpreter.asciiprint(solution)
    

if __name__ == '__main__':
    unittest.main()
