import sys
from itertools import product
from typing import List, Dict, Optional, Union
from csp import CSP, Constraint

def pretty_print(row: List[Union[str, int]]) -> None:
    print(''.join(['{:20s}'.format(str(s)) for s in row]))

def all_distinct(d: Dict[int, List[Union[str, int]]]) -> bool:
    vals: List[Union[str, List[Union[str, int]]]] = [d[k] for k in d]
    i : int ; j : int
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if not set(vals[i]).isdisjoint(vals[j]):
                return False
    return True

class LogicPuzzleConstraint(Constraint[int, List[Union[str, int]]]):
    def __init__(self, rows: List[int]) -> None:
        super().__init__(rows)
        self.rows: List[int] = rows

    def satisfied(self, assignment: Dict[int, List[Union[str, int]]]) -> bool:
        if not all_distinct(assignment):
            return False
        # Prolog style mneomic
        # [rose,_,_,mister_frostee]
        # [_,_,ice_pick,_]
        # [snowman,_,_,_]
        # [tree,220,chisel,_]
        # [_,_,_,_]
        # Clue 1.
        return True

if __name__ == '__main__':
    headers: List[str] = [ 'sculpture', 'pounds', 'tool', 'restaurant' ]
    sculptures: List[str] = [ 'basket', 'rose', 'snowman', 'swan', 'tree' ]
    pounds: List[int] = [ 180, 190, 200, 210, 220 ]
    tools: List[str] = ['chain saw', 'chisel', 'file', 'ice pick', 'ice scraper' ]
    restaurants: List[str] = [ 'arctic delight', 'chilly willys', 'freezer queen', 'frozen treats', 'mister frostee' ]
    row_nos: List[int] = [ 1, 2, 3, 4, 5 ]
    columns: List[List[Union[str, int]]] = [ list(col) for col in product(sculptures, pounds, tools, restaurants) ]
    #print(columns)
    domains: Dict[int, List[List[Union[str, int]]]] = { i: columns for i in row_nos }
    csp: CSP[int, List[Union[str, int]]] = CSP(row_nos, domains)
    csp.add_constraint(LogicPuzzleConstraint(row_nos))
    solution: Optional[Dict[int, List[Union[str, int]]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print('Solution found!')
        for row in solution:
            pretty_print(solution[row])
