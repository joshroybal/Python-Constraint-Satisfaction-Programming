import sys
from typing import List, Dict, Optional, Tuple
from csp import CSP, Constraint

def row(locations: Dict[Tuple[int, int], str], i: int) -> List[str]:
    r: int ; c: int
    return [locations[(r,c)] for (r,c) in locations if r == i]

def column(locations: Dict[Tuple[int, int], str], j: int) -> List[str]:
    r: int ; c: int
    return [locations[(r,c)] for (r,c) in locations if c == j]

# global variables
n: int = 3

class LatinSquareConstraint(Constraint[Tuple[int, int], str]):
    def __init__(self, places: List[Tuple[int, int]]) -> None:
        super().__init__(places)
        self.places: List[Tuple[int, int]] = places

    def satisfied(self, assignment: Dict[Tuple[int, int], str]) -> bool:
        for i in range(n):
            ir: List[str] = row(assignment, i)
            ic: List[str] = column(assignment, i)
            if len(ir) != len(set(ir)) or len(ic) != len(set(ic)):
                return False
        return True
    
if __name__ == "__main__":
    n = int(sys.argv[1])
    variables: List[Tuple[int, int]] = [(i, j) for i in range(n) for j in range(n)]
    domains: Dict[Tuple[int, int], List[str]] = {loc: [chr(65+i) for i in range(n)] for loc in variables}
    csp: CSP[Tuple[int, int], str] = CSP(variables, domains)
    csp.add_constraint(LatinSquareConstraint(variables))
    solution: Optional[Dict[Tuple[int, int], str]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print('Solution found!')
        for i in range(n):
            print(' '.join([solution[(i,j)] for j in range(n)]))
