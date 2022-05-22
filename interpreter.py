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

def _simplify(exp):
    if (type(exp) in (int,str,float)):
        return exp
    if all((type(i) in (str,int,float)) for i in tail(exp)) and any((type(i) is str) for i in tail(exp)):
        return exp
    try:
        return head(exp)(
            *map(simplify, tail(exp))
            )
    except OverflowError:
        return 0

def wrapper(func):
    def newfunc(*args):
        if any(type(i) not in (int,float) for i in args):
            return [func,*args]
        return func(*args)
        
    return newfunc
    
def simplify(exp):
    if type(exp) in (tuple,list):
        return wrapper(head(exp))(
            *map(simplify, tail(exp))
            )
    else:
        return exp

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

    
_count = 0
def _newname():
    global _count
    _count += 1
    return "CHILD"+str(_count)

#print a tree to a graph
def graphprint(exp, name="graph.gv"):
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
    dot.render('graph-output/'+name, view=True)

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
    #ret.append((slice(None),)) #can also get full tree
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

#recreate array, replacing item at idxs with newval
def with_subindex(exp, idxs, newval):
    if len(idxs) == 0:
        return newval
    else:
        return [*exp[:idxs[0]], with_subindex(exp[idxs[0]], idxs[1:], newval), *exp[idxs[0]+1:]]

import copy

#swap random subtrees between 2 trees
def crossover(exp1, exp2):
    sub_1 = random_subindex(exp1)
    sub_2 = random_subindex(exp2)
    oldexp1 = copy.deepcopy(exp1)
    exp1 = with_subindex(exp1, sub_1, access_subindex(exp2, sub_2))
    exp2 = with_subindex(exp2, sub_2, access_subindex(oldexp1, sub_1))
    return exp1, exp2

import matplotlib.pyplot as plt

# the main evolution loop
# attemps to evolve a tree to minimize the value of the fitness function, terminating when the selection cutoff is reached or 500 generations pass
# note that the selection cutoff uses normalized fitness ( 1/(1+raw fitness) ), so 1 is perfect
# if "verbose" is True on this will print out it's progress and plot it at the end
# templates
def evolve(functions, 
    terminals, 
    fitness_function, 
    pop_size=50, 
    init_max_depth=10, 
    crossover_rate=0.5, 
    selection_cutoff=0.99, 
    verbose=True,
    templates=((1, 'RANDOM'),)):  
    
    names = [t[1] for t in templates]
    weights = [t[0] for t in templates]
    population = []
    for _ in range(pop_size):
        name = random.choices(names, weights=weights)[0]
        if name=='RANDOM':
            population.append(randexp(functions, terminals, init_max_depth))
        else:
            population.append(name())
        
    xs = []
    ys = []
    
    for _ in range(50000):
        try:
            fitnesses = list(map(lambda p: 1/(1+fitness_function(p)), population))
            xs.append(_)
            ys.append(max(fitnesses))
            if verbose:
                print(_, max(fitnesses))
            if max(fitnesses)>selection_cutoff:
                break
            new_pop = []
            new_pop.append(population[fitnesses.index(max(fitnesses))])
            #print(sum(fitnesses))
            while len(new_pop) < pop_size:
                if random.random()<crossover_rate:
                    #new_pop.append(simplify(random.choices(population, weights = fitnesses, k=1)[0]))
                    for i in crossover(*random.choices(population, weights = fitnesses, k=2)):
                        new_pop.append(i)
                else:
                    new_pop.append(*random.choices(population, weights = fitnesses, k=1))
            population = new_pop
        except KeyboardInterrupt:
            break
    
    if verbose:
        fig, ax = plt.subplots()
        ax.plot(xs, ys)
        ax.set(xlabel='generation', ylabel='max fitness',
               title='max fitness per generation')
        ax.grid()

        fig.savefig("test.png")
        plt.show()
    
    #print(fitnesses.index(max(fitnesses)))
    return population[fitnesses.index(max(fitnesses))]
        