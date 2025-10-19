# early_risers.py
from typing import List, Dict, Optional
from itertools import product
from csp import CSP, Constraint

def pretty_print(d: Dict[str, List[str]]) -> None:
    for k in d:
        print(''.join(['{:20s}'.format(s) for s in [str(k)] + d[k]]))
       
def all_distinct(d: Dict[str, List[str]]) -> bool:
    checked: List[List[str]] = []
    for key in d:
        for t in checked:
            for item in d[key]:
                if item in t:
                    return False
        checked.append(d[key])
    return True

def is_woman(name: str) -> bool:
    return name in ['Belinda', 'Martha']

def is_man(name: str) -> bool:
    return name in ['Bob', 'Peter', 'Tim']

def implies(p: bool, q: bool) -> bool:
    return not p or q

def equivalent(p: bool, q:bool) -> bool:
    return implies(p, q) and implies(q, p)

def reduce(t: List[int]) -> int:
    acc: int = 1
    for i in t:
        acc *= i
    return acc

# Fumbling towards AC3.
def prune(d: Dict[str, List[List[str]]]) -> None:
    for name in d:
        d[name] = [ v for v in d[name] if implies(name == 'Bob', 'Chief Clerk' in v) ]
        d[name] = [ v for v in d[name] if implies(name == 'Bob', '1859' not in v) ]
        d[name] = [ v for v in d[name] if equivalent('1848' in v, 'Novelist' in v) ]
        d[name] = [ v for v in d[name] if implies(name == 'Bob', '1849' not in v) ]
        d[name] = [ v for v in d[name] if implies('1849' in v, is_man(name)) ]
        d[name] = [ v for v in d[name] if implies(name == 'Belinda', '1850' in v) ]
        d[name] = [ v for v in d[name] if implies(name == 'Tim', '1848' not in v and '1849' not in v) ]
        d[name] = [ v for v in d[name] if implies(name == 'Tim', 'Clapham' not in v and 'Camden Town' not in v) ]
        d[name] = [ v for v in d[name] if equivalent('Hotelier' in v, 'Camden Town' in v) ]
        d[name] = [ v for v in d[name] if implies('Hotelier' in v, '1849' not in v and '1859' not in v) ]
        d[name] = [ v for v in d[name] if implies(name == 'Bob', 'Missionary' not in v) ]
        d[name] = [ v for v in d[name] if implies('Missionary' in v, 'Paddington' not in v) ]
        d[name] = [ v for v in d[name] if equivalent('1851' in v, 'Highbury' in v) ]
        d[name] = [ v for v in d[name] if implies(name == 'Martha', 'Greenwich' in v) ]
        
# Save this - this was by far the empirically best processing ordering!
class LogicPuzzleConstraint(Constraint[str, List[str]]):
    def __init__(self, variables: List[str]) -> None:
        super().__init__(variables)
        self.variables: List[str] = variables

    def satisfied(self, assignment: Dict[str, List[str]]) -> bool:
        if not all_distinct(assignment):
            return False
        return True

if __name__ == '__main__':
    names: List[str] = ['Belinda', 'Bob', 'Martha', 'Peter', 'Tim']
    jobs: List[str] = ['Chief Clerk', 'Hotelier', 'Missionary', 'Novelist', 'Teacher']
    years: List[str] = ['1848', '1849', '1850', '1851', '1859']
    districts: List[str] = ['Camden Town', 'Clapham', 'Greenwich', 'Highbury', 'Paddington']
    domains: Dict[str, List[List[str]]] = { name: [list(t) for t in list(product(jobs, years, districts))] for name in names }
    prune(domains)
    csp: CSP[str, List[str]] = CSP(names, domains)
    csp.add_constraint(LogicPuzzleConstraint(names))
    solution: Optional[Dict[str, List[str]]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print('Solution found!')
        pretty_print(solution)
