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
        # Prolog style mnemonic
        # [_,_,_,_]
        # [_,_,_,_]
        # [_,_,_,_]
        # [_._,_,_]
        # numerical relation flags
        blue_pos: int = 0 ; tan_pos: int = 0 ; starfish_pos: int = 0; 
        for row in assignment:
            x = assignment[row] ; position = x[-1]
            if 'crab' in x and 'green' in x:
                return False
            if (2 in x or 3 in x) and ('crab' in x or 'green' in x):
                return False
            if 'blue' in x and ('sand dollar' in x or 'scallop' in x):
                return False
            if 'sea horse' in x and 'nautilus' in x:
                return False
            if 'conch' in x and ('blue' in x or 'tan' in x or 1 in x or 4 in x):
                return False
            if 'crab' in x and ('nautilus' in x or 'turban' in x):
                return False
            if 'starfish' in x and 'tan' in x:
                return False
            if 'blue' in x:
                blue_pos = int(position)
            if 'tan' in x:
                tan_pos = int(position)
            if 'starfish' in x:
                starfish_pos = int(position)
        # numerical relation checks
        if blue_pos > 0 and tan_pos > 0:
            if abs(blue_pos - tan_pos) != 2:
                return False
        if tan_pos > 0 and starfish_pos > 0:
            if not starfish_pos is tan_pos - 1:
                return False
        return True

if __name__ == '__main__':
    headers: List[str] = [ 'creature', 'seashell', 'color', 'position' ]
    creature: List[str] = [ 'crab', 'sand dollar', 'sea horse', 'starfish' ]
    seashell: List[str] = [ 'conch', 'nautilus', 'scallop', 'turban' ]
    color: List[str] = [ 'blue', 'green', 'tan', 'yellow' ]
    position: List[int] = [ 1, 2, 3, 4 ]
    row_nos: List[int] = [ 1, 2, 3, 4 ]
    columns: List[List[Union[str, int]]] = [ list(col) for col in product(creature, seashell, color, position) ]
    domains: Dict[int, List[List[Union[str, int]]]] = { i: columns for i in row_nos }
    csp: CSP[int, List[Union[str, int]]] = CSP(row_nos, domains)
    csp.add_constraint(LogicPuzzleConstraint(row_nos))
    solution: Optional[Dict[int, List[Union[str, int]]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print('Solution found!')
        sub: Dict[Union[str, int], str] = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth'}
        for row in solution:
            solution[row][-1] = sub[solution[row][-1]]
        for row in solution:
            pretty_print(solution[row])
