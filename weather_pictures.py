# logic_puzzle.py
from typing import List, Dict, Optional, Tuple
from itertools import product
from csp import CSP, Constraint

def all_distinct(d: Dict[str, Tuple[str, str, str]]) -> bool:
    checked: List[Tuple[str, str, str]] = []
    for key in d:
        #if d[key] in checked:
        #    return False
        for t in checked:
            for item in d[key]:
                if item in t:
                    return False
        checked.append(d[key])
    return True

def is_man(name: str) -> bool:
    return name in ['Henry', 'Richard']

def is_woman(name: str) -> bool:
    return name in ['Josephine', 'Marjorie']

class LogicPuzzleConstraint(Constraint[str, Tuple[str, str, str]]):
    def __init__(self, variables: List[str]) -> None:
        super().__init__(variables)
        self.variables: List[str] = variables

    def satisfied(self, assignment: Dict[str, Tuple[str, str, str]]) -> bool:
        if len(assignment) != len(set(assignment)):
            return False
        if not all_distinct(assignment):
            return False
        if len(assignment) == 4:
            #print(assignment)
            # 1.
            if 'Henry' in assignment['Monday']: 
                return False
            if 'rainbow' in assignment['Thursday']: 
                return False
            if 'Henry' in assignment['Tuesday'] and 'rainbow' not in assignment['Monday']:
                return False
            # 3.
            if 'Richard' not in assignment['Thursday'] or 'sunshine' in assignment['Thursday']:
                return False
            # 4.
            if 'thunderstorm' in assignment['Monday'] or 'lake' in assignment['Thursday']:
                return False
            if 'thunderstorm' in assignment['Tuesday'] and 'lake' not in assignment['Monday']:
                return False
            
        for day in assignment:
            t = assignment[day]
            # 1.
            if 'rainbow' in t and ('Henry' in t or 'hills' not in t):
                return False
            # 2.
            if 'Josephine' in t and 'city' not in t:
                return False
            # 4.
            if 'thunderstorm' in t and not is_woman(t[2]):
                return False
        return True# logic_puzzle.py

if __name__ == '__main__':
    variables: List[str] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday']
    features: List[str] = ['rainbow', 'sunset', 'sunshine', 'thunderstorm']
    settings: List[str] = ['city', 'hills', 'lake', 'river']
    names: List[str] = ['Henry', 'Josephine', 'Marjorie', 'Richard']
    domains: Dict[str, List[Tuple[str, str,str]]] = {v: list(product(features, settings, names)) for v in variables}
    csp: CSP[str, Tuple[str, str, str]] = CSP(variables, domains)
    csp.add_constraint(LogicPuzzleConstraint(variables))
    solution: Optional[Dict[str, Tuple[str, str, str]]] = csp.backtracking_search()
    
    if solution is None:
        print('No solution found!')
    else:
        print('Solution found!')
        #print(solution)
        for day in solution:
            print(day, ':', solution[day])
