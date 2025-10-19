import sys
from csp import Constraint, CSP
from typing import Dict, List, Optional, Tuple

def row(locations: Dict[Tuple[int, int], str], i: int) -> List[str]:
    r: int ; c: int
    return [ locations[(r,c)] for (r,c) in locations if r == i ]

def column(locations: Dict[Tuple[int, int], str], j: int) -> List[str]:
    r: int ; c: int
    return [ locations[(r,c)] for (r,c) in locations if c == j ]

def box(locations: Dict[Tuple[int, int], str], row: int, col: int) -> List[str]:
    i: int ; j: int ; r: int ; c: int
    i, j = 3 * (row // 3), 3 * (col // 3)
    return [locations[(r,c)] for (r,c) in locations if r in range(i,i+3) and c in range(j,j+3)]

def readfile(filename: str) ->  Dict[Tuple[int, int], List[str]]:
    f = open(filename, 'r')
    rows: List[List[str]] = [row.strip().split(',') for row in f.readlines()]
    f.close()
    domains:  Dict[Tuple[int, int], List[str]] = {}
    i: int ; j: int
    for i in range(9):
        for j in range(9):
            domains[(i,j)] = [rows[i][j]] if rows[i][j] != '' else [str(n) for n in range(1, 10) ]
    # restrict domains first in order to lighten load on constraint satisfaction
    for t in domains:
        if len(domains[t]) == 1:
            number: str = domains[t][0]
            i, j = t
            ith_row: List[List[str]] = [domains[(i,j)] for j in range(9)]
            for x in ith_row:
                if len(x) > 1 and number in x:
                    x.remove(number)

            jth_col: List[List[str]] = [domains[(i,j)] for i in range(9)]
            for x in jth_col:
                if len(x) > 1 and number in x:
                    x.remove(number)

            i = 3 * (i // 3) ; j = 3  * (j // 3)
            r: int ; c: int
            ij_box: List[List[str]] = [domains[(r,c)] for r in range(i,i+3) for c in range(j,j+3)]
            for x in ij_box:
                if len(x) > 1 and number in x:
                    x.remove(number)
    return domains


class NumberPlaceConstraint(Constraint[Tuple[int, int], str]):
    def __init__(self, places: List[Tuple[int, int]]) -> None:
        super().__init__(places)
        self.places: List[Tuple[int, int]] = places

    def satisfied(self, assignment: Dict[Tuple[int, int], str]) -> bool:
        i: int ; j : int

        for i in range(9):
            ith_row: List[str] = row(assignment, i)
            if len(ith_row) != len(set(ith_row)):
                return False
            ith_col: List[str] = column(assignment, i)
            if len(ith_col) != len(set(ith_col)):
                return False

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                nth_box: List[str] = box(assignment, i, j)
                if len(nth_box) != len(set(nth_box)):
                    return False
        return True

if __name__ == "__main__":
    n: int = 9
    variables: List[Tuple[int, int]] = [(i,j) for i in range(n) for j in range(n)]
    domains:  Dict[Tuple[int, int], List[str]] = readfile(sys.argv[1])
    print(domains)
    csp: CSP[Tuple[int, int], str] = CSP(variables, domains)
    csp.add_constraint(NumberPlaceConstraint(variables))
    solution: Optional[Dict[Tuple[int, int], str]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print('solution')
        print(solution)
        for i in range(n):
            print(' '.join([solution[(i,j)] for j in range(n)]))
