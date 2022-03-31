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

def interpret(exp, definitions=None):
    if (type(exp) is int) or (type(exp) is float):
        return exp
    if type(exp) is str:
        return definitions[exp]
    try:
        return head(exp)(
            *map(lambda e: interpret(e, definitions), tail(exp))
            )
    except OverflowError:
        return 0

def asciiprint(exp):
    def _asciiprint(exp, indent=0):
        if (type(exp) is int) or (type(exp) is float) or (type(exp) is str):
            return "|"*indent+str(exp)
        elif callable(exp):
            return "|"*indent+exp.__name__
        else:
            return "\n".join((
                _asciiprint(head(exp), indent),
                *(_asciiprint(arg, indent+1) for arg in tail(exp)),
                ))
    return _asciiprint(exp, indent=0)

def randexp(F, T, maxdepth=5):
    U = list(F.union(T))
    def _randexp(atom, depth=2):
        if atom in T:
            return atom
        if atom in F:
            return (atom, *[_randexp(
                random.choice(U) if depth<maxdepth else random.choice(list(T)), depth+1
                ) for _ in range(nargs(atom))])
    return _randexp(random.choice(list(F)))
    
_count = 0
def _newname():
    global _count
    _count += 1
    return "CHILD"+str(_count)

def graphprint(exp):
    dot = graphviz.Digraph()

    def _graphprint(exp, parentname):
        if type(exp) in (tuple, list):
            for child in tail(exp):
                childname = _newname()
                dot.node(
                    childname,
                    head(child).__name__ if (type(child) in (tuple, list)) else str(child)
                    )
                dot.edge(parentname, childname)
                _graphprint(child, childname)
            
    dot.node("PARENT", head(exp).__name__)
    _graphprint(exp, "PARENT")
    dot.render('graph-output/graph.gv', view=True)

# return the indexes for all subtrees of an expression, to use in crossover
# ex. for the expression [+ [ln 2] [* 2 3]] it would return:
# (1,) , (2,) , (1,1) , (2,1) , (2,2) 
# as there are subtrees at exp[1], exp[2], exp[1][1], exp[2][1], and exp[2][2] but no more
def get_subindices(exp):
    ret = []
    curr = [(_,) for _ in range(1,1+nargs(exp[0]))]
    while len(curr) > 0:
        for i, idxs in enumerate(curr):
            subtree = access_subindex(exp, idxs)
            if type(subtree) in (tuple, list):
                ret.append(idxs)
                del curr[i]
                for i in range(1,1+nargs(subtree[0])):
                    curr.append(idxs+(i,))
            else:
                ret.append(idxs)
                del curr[i]
    ret.append((slice(None),)) #can also get full tree
    return ret

# return a radom subindex of a expression
def random_subindex(exp):
    return random.choice(get_subindices(exp))

# access a subtree of an index by indices
# ex. access_subindex(exp, (1,3,4,2,1)) would return exp[1][3][4][2][1] 
def access_subindex(exp, idxs):
    ret = exp#[:]
    for i in idxs:
        ret = ret[i]
    return ret

'''
def mod_subindex(exp, idxs, newval):
    for i in idxs:
        exp = exp[i]
    print("exp:"+str(exp))
    exp = newval

def crossover(exp1, exp2):
    modify_subindex(exp1, (1,), "TESTING")


def modify_subindex(exp, idxs, newval):
    if len(idxs) == 0:
        exp = newval
    else:
        modify_subindex(exp[idxs[0]], idxs[1:], newval)
        '''

#recreate array with idxes
def with_subindex(exp, idxs, newval):
    print(exp)
    if len(idxs) == 0:
        return newval
    else:
        return [*exp[:idxs[0]], with_subindex(exp[idxs[0]], idxs[1:], newval), *exp[idxs[0]+1:]]

#bad! ugly!
'''
def set_subindex(exp, idxs, newval):
   exec("exp"+"".join("["+str(i)+"]" for i in idxs)+" = newval", locals())'''

a = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]
a = with_subindex(a, (2,), 100)
print("modified: "+str(a))
    
    