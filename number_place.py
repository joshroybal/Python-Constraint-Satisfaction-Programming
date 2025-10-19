# number_place.py
from math import sqrt
from csp import Constraint, CSP
from typing import Dict, List, Optional, Tuple

def row(locations: Dict[Tuple[int, int], str], i: int) -> List[Tuple[int, int]]:
    r: int ; c: int
    return [ (r,c) for (r,c) in locations if r == i ]

def column(locations: Dict[Tuple[int, int], str], j: int) -> List[Tuple[int, int]]:
    r: int ; c: int
    return [ (r,c) for (r,c) in locations if c == j ]

def box(locations: Dict[Tuple[int, int], str], row: int, col: int) -> List[Tuple[int, int]]:
    i: int ; j: int ; r: int ; c: int
    i, j = 3 * (row // 3), 3 * (col // 3)
    return [(r,c) for (r,c) in locations if r in range(i,i+3) and c in range(j,j+3)]


class NumberPlaceConstraint(Constraint[Tuple[int, int], str]):
    def __init__(self, places: List[Tuple[int, int]]) -> None:
        super().__init__(places)
        self.places: List[Tuple[int, int]] = places

    def satisfied(self, assignment: Dict[Tuple[int, int], str]) -> bool:
        for n in range(9):
            nth_row = [assignment[x] for x in row(assignment, n)]
            nth_col = [assignment[x] for x in column(assignment, n)]
            if len(nth_row) != len(set(nth_row)) or len(nth_col) != len(set(nth_col)):
                return False
        i: int ; j : int
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                nth_box = [assignment[x] for x in box(assignment, i, j)]
                if len(nth_box) != len(set(nth_box)):
                    return False

        return True

if __name__ == "__main__":
    n: int = 9
    variables: List[Tuple[int, int]] = [(i,j) for i in range(n) for j in range(n)]
    domains: Dict[Tuple[int, int], List[str]] = {}
    for variable in variables:
        domains[variable] = [ str(k+1) for k in range(n) ]
    csp: CSP[Tuple[int, int], str] = CSP(variables, domains)
    csp.add_constraint(NumberPlaceConstraint(variables))
    solution: Optional[Dict[Tuple[int, int], str]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print('solution')
        for i in range(n):
            print(' '.join([solution[(i,j)] for j in range(n)]))
