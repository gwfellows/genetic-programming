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

print(
interpreter.get_subindices([add, [ln, 2], [mul, 2, 3]])
)

print(
interpreter.get_subindices([ln, 1])
)

print(
interpreter.get_subindices([exp, [exp, 1, 2], [exp, 2, 2]])
)

a = [div, [sub, [exp, 'X', 'Y'], 10], 3]
b = [add, [mul, 'X', 2], 10]

print(interpreter.asciiprint(a))
print("\n\n")
print(interpreter.asciiprint(b))
print("\n\n")
print("\n\n")

interpreter.crossover(a,b)
#a = interpreter.access_subindex(a, (1,))
#a = "TESTING"

print(interpreter.asciiprint(a))
print("\n\n")
print(interpreter.asciiprint(b))


'''

import unittest

class Test(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
'''