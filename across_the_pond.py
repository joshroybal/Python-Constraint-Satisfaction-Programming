#!/usr/bin/env python3
# across_the_pond.py

from itertools import product
from typing import List, Dict, Optional, Tuple, Set
from csp import CSP, Constraint

def disjoint_lists_p(t: List[List[str]]) -> bool:
    checked: Set[str] = set()
    for sublist in t:
        for string in sublist:
            if string in checked:
                return False
            checked.add(string)
    return True

class LogicPuzzleConstraint(Constraint[str, List[str]]):
    def __init__(self, names: List[str]) -> None:
        super().__init__(names)
        self.names: List[str] = names

    def satisfied(self, assignment: Dict[str, List[str]]) -> bool:
        t = []
        for name in assignment:
            t.append(assignment[name])
            if t.count(assignment[name]) > 1:
                return False
        if not disjoint_lists_p(t):
            return False
        if 'Val' in assignment:
            if 'Yorkshire' in assignment['Val']:
                return False
            if 'Poughkeepsie' in assignment['Val']:
                return False
            if 'Levittown' in assignment['Val']:
                return False
            if 'May' in assignment['Val'] or 'June' in assignment['Val']:
                return False
        if 'Peg' in assignment:
            if 'Amsterdam' in assignment['Peg']:
                return False
            if 'Essex' in assignment['Peg'] or 'Kent' in assignment['Peg']:
                return False
        if 'Liz' in assignment:
            if 'May' in assignment['Liz'] or 'Somerset' in assignment['Liz'] or 'June' in assignment['Liz']:
                return False
        essex_row: List[str] = []
        levittown_row: List[str] = []
        poughkeepsie_row: List[str] = []
        yorkshire_row: List[str] = []
        for name in assignment:
            if {'Poughkeepsie', 'Yorkshire'} <= set(assignment[name]):
                return False
            if {'Poughkeepsie', 'July'} <= set(assignment[name]):
                return False
            if {'Poughkeepsie', 'August'} <= set(assignment[name]):
                return False            
            if {'May', 'Somerset'} <= set(assignment[name]):
                return False
            if {'May', 'Yorkshire'} <= set(assignment[name]):
                return False            
            if {'Amsterdam', 'Essex'} <= set(assignment[name]):
                return False
            if {'Amsterdam', 'Kent'} <= set(assignment[name]):
                return False
            if {'Essex', 'Levittown'} <= set(assignment[name]):
                return False
            if {'Essex', 'August'} <= set(assignment[name]):
                return False
            if {'Somerset', 'August'} <= set(assignment[name]):
                return False
            if {'May', 'Levittown'} <= set(assignment[name]):
                return False            
            if 'Essex' in assignment[name]:
                essex_row = assignment[name]
            if 'Levittown' in assignment[name]:
                levittown_row = assignment[name]
            if 'Poughkeepsie' in assignment[name]:
                poughkeepsie_row = assignment[name]
            if 'Yorkshire' in assignment[name]:
                yorkshire_row = assignment[name]
                
        #months: List[str] = ['May', 'June', 'July', 'August']
        if len(essex_row) == 3 and len(levittown_row) == 3:
            if 'May' in essex_row and 'June' not in levittown_row:
                return False
            if 'June' in essex_row and 'July' not in levittown_row:
                return False
            if 'July' in essex_row and 'August' not in levittown_row:
                return False        
        return True

if __name__ == '__main__':
    columns: List[str] = ['name', 'town', 'county', 'month']
    rows: List[int] = [i for i in range(len(columns))]
    names: List[str] = ['Amy', 'Liz', 'Peg', 'Val' ]
    towns: List[str] = ['Albany', 'Amsterdam', 'Levittown', 'Poughkeepsie']
    counties: List[str] = ['Essex', 'Kent', 'Somerset', 'Yorkshire']
    months: List[str] = ['May', 'June', 'July', 'August']

    # x: Set[str] = set(towns)
    # y: Set[str] = set(counties)
    # z: Set[str] = set(months)
    # for ele in product(x, y, z):
    #     print(ele)

    domains: Dict[str, List[List[str]]] = {}
    #print(domains)
    for ele in product(names, towns, counties, months):
        #print(list(ele))
        x = list(ele)
        domains.setdefault(x[0], []).append(x[1:])
    #print(domains)
    #for key in domains:
    #    print(key, domains[key])
    #quit()
    
    #table: List[List[List[str]]] = [[names,towns,counties,months] for i in rows]
    #m: int = len(table) ; n: int = len(columns)
    #domains: Dict[Tuple[int, int], List[str]] = {(i, j): table[i][j] for i in range(m) for j in range(n)}

    #cells = [ cell for cell in domains ]
    csp: CSP[str, List[str]] = CSP(names, domains)
    csp.add_constraint(LogicPuzzleConstraint(names))
    solution: Optional[Dict[str, List[str]]] = csp.backtracking_search()
    if solution is not None:
        print(solution)
        for name in solution:
            print([name] + solution[name])
