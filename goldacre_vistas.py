# logic_puzzle.py
from typing import List, Dict, Optional, Tuple
from itertools import product
from csp import CSP, Constraint

def all_distinct(d: Dict[int, Tuple[str, str, str]]) -> bool:
    checked: List[Tuple[str, str, str]] = []
    for key in d:
        for t in checked:
            for item in d[key]:
                if item in t:
                    return False
        checked.append(d[key])
    return True

def implies(p: bool, q: bool) -> bool:
    return not p or q

def equivalent(p: bool, q: bool) -> bool:
    return implies(p, q) and implies(q, p)

def is_man(name: str) -> bool:
    return name in ['Cedric', 'Horatio', 'Peter', 'brother', 'butler', 'uncle']

def is_woman(name: str) -> bool:
    return name in ['Betty', 'Rowena', 'Violet', 'daughter', 'governess', 'wife']

def clockwise(i: int, j: int) -> bool:
    return j - i == 1 or j - i == -5

def adjacent(i: int, j: int) -> bool:
    return abs(i - j) == 1 or abs(i - j) == 5

def is_odd(n: int) -> bool:
    return n % 2 == 1

def prune(domains: Dict[int, List[Tuple[str, str, str]]]) -> None:
    #domains[2] = [ v for v in domains[2] if 'Horatio' in v ]
    #domains[6] = [ v for v in domains[6] if 'lake' in v ]
    for i in domains:
        domains[i] = [(n,c,f) for (n,c,f) in domains[i] if equivalent(is_man(n), is_man(c)) and equivalent(is_woman(n), is_woman(c)) ]
        domains[i] = [ v for v in domains[i] if equivalent('Cedric' in v, 'butler' in v) ]
        domains[i] = [ v for v in domains[i] if implies('statues' in v, 'Betty' not in v) ]
        domains[i] = [ v for v in domains[i] if implies('Violet' in v, is_odd(i)) ]
        domains[i] = [ v for v in domains[i] if equivalent('Violet' in v, 'gates' in v) ]
        domains[i] = [ v for v in domains[i] if implies('temple' in v, is_man(v[0]) and is_man(v[1])) ]
        domains[i] = [ v for v in domains[i] if implies('grotto' in v, is_woman(v[0]) and is_woman(v[1])) ]
        domains[i] = [ v for v in domains[i] if implies('governess' in v, i > 2) ]
        domains[i] = [ v for v in domains[i] if implies('Horatio' in v, i == 2) ]
        domains[i] = [ v for v in domains[i] if implies('lake' in v, i == 5) ]
        domains[i] = [ v for v in domains[i] if equivalent(i == 4, 'daughter' in v) ]
        domains[i] = [ v for v in domains[i] if implies('daughter' in v, 'waterfall' not in v) ]
    domains[2] = [ v for v in domains[2] if 'Horatio' in v ]
    domains[5] = [ v for v in domains[5] if 'lake' in v ]
    domains[4] = [ v for v in domains[4] if 'daughter' in v ]

# Save this - this was by far the empirically best processing ordering!
class LogicPuzzleConstraint(Constraint[int, Tuple[str, str, str]]):
    def __init__(self, variables: List[int]) -> None:
        super().__init__(variables)
        self.variables: List[int] = variables

    def satisfied(self, assignment: Dict[int, Tuple[str, str, str]]) -> bool:
        if not all_distinct(assignment):
            return False

        CedricVista: int ; StatuesVista: int
        violet_vista: int ; temple_vista: int
        uncle_vista : int ; brother_vista: int
        for vista in assignment:
            if 'Cedric' in assignment[vista]:
                CedricVista = vista
            if 'statues' in assignment[vista]:
                StatuesVista = vista
            if 'Violet' in assignment[vista]:
                violet_vista = vista
            if 'temple' in assignment[vista]:
                temple_vista = vista
            if 'uncle' in assignment[vista]:
                uncle_vista = vista
            if 'brother' in assignment[vista]:
                brother_vista = vista
        if len(assignment) == 6:
            if not clockwise(StatuesVista, CedricVista):
                return False
            if adjacent(violet_vista, temple_vista):
                return False
            if uncle_vista != 1 + brother_vista:
                return False
        return True

if __name__ == '__main__':
    variables: List[int] = [1, 2, 3, 4, 5, 6]
    names: List[str] = ['Betty', 'Cedric', 'Horatio', 'Peter', 'Rowena',
                        'Violet']
    connections: List[str] = ['brother', 'butler', 'daughter', 'governess',
                              'uncle', 'wife']
    features: List[str] = ['statues', 'lake', 'temple', 'grotto', 'waterfall',
                           'gates']
    domains: Dict[int, List[Tuple[str, str,str]]] = {v: list(product(names, connections, features)) for v in variables}
    print([ len(domains[variable]) for variable in variables ])
    prune(domains)
    print([ len(domains[variable]) for variable in variables ])
    #quit()
    csp: CSP[int, Tuple[str, str, str]] = CSP(variables, domains)
    csp.add_constraint(LogicPuzzleConstraint(variables))
    solution: Optional[Dict[int, Tuple[str, str, str]]] = csp.backtracking_search()

    if solution is None:
        print('No solution found!')
    else:
        print('Solution found!')
        #print(solution)
        for vista in solution:
            print(vista, ':', solution[vista])
