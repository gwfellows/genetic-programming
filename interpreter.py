import random
import math
from inspect import signature
import graphviz


def head(exp):
    return exp[0]

def tail(exp):
    return exp[1:]

def nargs(func):
    return len(signature(func).parameters)

def interpret(exp, definitions={}):
    if (type(exp) is int) or (type(exp) is float):
        return exp
    if type(exp) is str:
        return definitions[exp]
    return head(exp)(
        *map(lambda e: interpret(e, definitions), tail(exp))
        )

def asciiprint(exp, indent=0):
    if (type(exp) is int) or (type(exp) is float):
        print("|"*indent+str(exp))
    elif callable(exp):
        print("|"*indent+exp.__name__)
    else:
        asciiprint(head(exp), indent)
        for arg in tail(exp):
            asciiprint(arg, indent+1)
    
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

FUNCTIONS = {add, sub, mul, div, sqrt, exp, ln}
TERMINALS = {0,1,2,3,4,5,6,7,8,9}

def randexp(F, T):
    U = list(F.union(T))
    def _randexp(atom):
        print(atom)
        if atom in T:
            return atom
        if atom in F:
            return (atom, *[_randexp(random.choice(U)) for _ in range(nargs(atom))])
    return _randexp(random.choice(list(F)))
    
_count = 0
def _newname():
    global count
    _count += 1
    return "CHILD"+str(count)

def graphprint(exp):
    dot = graphviz.Digraph()

    def _graphprint(exp, parentname):
        if type(exp) is tuple:
            for child in tail(exp):
                childname = _newname()
                dot.node(
                    childname,
                    head(child).__name__ if (type(child) is tuple) else str(child)
                    )
                dot.edge(parentname, childname)
                _graphprint(child, childname)
            
    dot.node("PARENT", head(exp).__name__)
    _graphprint(exp, "PARENT")
    dot.render('graph-output/graph.gv', view=True)
