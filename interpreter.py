#from operator import *

def head(exp):
    return exp[0]

def tail(exp):
    return exp[1:]

def interpret(exp):
    if type(exp) is int:
        return exp
    else:
        return head(exp)(
            *map(interpret, tail(exp))
            )

def prettyprint(exp, indent=0):
    if type(exp) is int:
        print(" "*indent+str(exp))
    elif callable(exp):
        print(" "*indent+exp.__name__)
    else:
        prettyprint(head(exp), indent)
        for arg in tail(exp):
            prettyprint(arg, indent+3)

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
    return a**b;

def ln(a):
    if a<=0:
        return 0
    return math.log(a)

"""
print(
    interpret(
        (add, (sub, 9, 1), (mul, 20, (div, 9, 6))),
    )
)

prettyprint(
    (add, (sub, 9, 1), (mul, 20, (div, 9, 6))),
)
"""
