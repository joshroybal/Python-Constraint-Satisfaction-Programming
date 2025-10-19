# early_risers.py
from typing import List, Dict, Optional
from itertools import product
from csp import CSP, Constraint

#def pretty_print(row: List[Union[str, int]]) -> None:
#    print(''.join(['{:20s}'.format(str(s)) for s in row]))

def pretty_print(d: Dict[str, List[str]]) -> None:
    for k in d:
        print(''.join(['{:33s}'.format(s) for s in [str(k)] + d[k]]))

def all_distinct(d: Dict[str, List[str]]) -> bool:
    t = [ e for l in [ d[k] for k in d ] for e in l ]
    if len(t) != len(set(t)):
        return False
    else:
        return True

def imp(p: bool, q: bool) -> bool:
    return not p or q

def eqv(p: bool, q: bool) -> bool:
    return imp(p, q) and imp(q, p)

def prune(d: Dict[str, List[List[str]]]) -> None:
    for k in d:
        d[k] = [ v for v in d[k] if imp(k == 'Signal box', 'Raggindale' not in v) ]
        d[k] = [ v for v in d[k] if eqv(k == 'Signal box', 'Bought from museum' in v) ]
        d[k] = [ v for v in d[k] if eqv(k == 'Lamp posts', 'Ostermoor' in v) ]
        d[k] = [ v for v in d[k] if eqv('Bought from demolisher' in v, '1908' in v) ]
        d[k] = [ v for v in d[k] if imp('1900' in v, k != 'Footbridge' and 'Salvaged from scrap' not in v) ]
        d[k] = [ v for v in d[k] if imp('1904' in v, 'Hancaster' not in v) ]
        d[k] = [ v for v in d[k] if eqv('1894' in v, 'Dottingley' in v) ]
        d[k] = [ v for v in d[k] if imp(k == 'Indicator board', int(v[1]) < 1900) ]

class LogicPuzzleConstraint(Constraint[str, List[str]]):
    def __init__(self, variables: List[str]) -> None:
        super().__init__(variables)
        self.variables: List[str] = variables

    def satisfied(self, assignment: Dict[str, List[str]]) -> bool:
        if not all_distinct(assignment):
            return False
      
        if 'Clock' in assignment and 'Lamp posts' in assignment and int(assignment['Clock'][1]) < int(assignment['Lamp posts'][1]):
            return False
       
        raggindale_date: int = 0
        museum_date: int = 0
        scrap_date: int = 0
        auction_date: int = 0
        for v in assignment:
            location, date, means = assignment[v]
            if 'Raggindale' == location:
                raggindale_date = int(date)
            if 'Bought from museum' == means:
                museum_date = int(date)
            if means == 'Salvaged from scrap':
                scrap_date = int(date)
            if means == 'Bought at auction':
                auction_date = int(date)            
            
        if museum_date != 0 and raggindale_date != 0 and (museum_date - raggindale_date != 4):
                return False
        if auction_date != 0 and scrap_date != 0 and (scrap_date < auction_date):
            return False
      
        return True

if __name__ == '__main__':
    acquisitions: List[str] = ['Clock', 'Footbridge', 'Indicator board', 'Lamp posts', 'Signal box']
    locations: List[str] = ['Dottingley', 'Gorsemont', 'Hancaster', 'Ostermoor', 'Raggindale']
    dates: List[str] = ['1894', '1898', '1900', '1904', '1908']
    means: List[str] = ['Bought at auction', 'Bought from demolisher', 'Bought from museum', 'Donated by benefactor', 'Salvaged from scrap']
    domains: Dict[str, List[List[str]]] = { acquisition: [list(t) for t in list(product(locations, dates, means))] for acquisition in acquisitions }
    print([ len(domains[k]) for k in domains ])
    prune(domains)
    print([ len(domains[k]) for k in domains ])
    #print(domains)
    csp: CSP[str, List[str]] = CSP(acquisitions, domains)
    csp.add_constraint(LogicPuzzleConstraint(acquisitions))
    solution: Optional[Dict[str, List[str]]] = csp.backtracking_search()

    if solution is None:
        print('No solution found!')
    else:
        print('Solution found!')
        #print(solution)
        pretty_print(solution)
