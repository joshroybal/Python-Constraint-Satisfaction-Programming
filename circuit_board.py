from typing import NamedTuple, List, Dict, Optional, Tuple
from csp import CSP, Constraint

Grid = List[List[str]]  # type alias for grids

class GridLocation(NamedTuple):
    row: int
    column: int

def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with X for no chip on that square
    return [['....' for c in range(columns)] for r in range(rows)]

def display_grid(grid: Grid) -> None:
    for row in grid:
        print('|' + '|'.join(row) + '|')

def generate_domain(chip: Tuple[str, Tuple[int,int]], grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    (m, n) = chip[1]
    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + n)
            rows: range = range(row, row + m)
            if col + n + 1 <= width and row + n + 1 <= height:
                domain.append([GridLocation(r, c) for c in columns for r in rows])
    return domain


class CircuitBoardConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, chips: List[str]) -> None:
        super().__init__(chips)
        self.chips: List[str] = chips

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        # if there are any duplicates grid locations then there is an overlap
        all_locations = [locs for values in assignment.values() for locs in values]
        return len(set(all_locations)) == len(all_locations)

if __name__ == "__main__":
    grid: Grid = generate_grid(9, 9)
    chips: Dict[str, Tuple[int,int]] = {'8080':(2,5),'6502':(2,2),'6800':(4,4),' Z80':(3,3),'6809':(6,1)}
    locations: Dict[str, List[List[GridLocation]]] = {}
    for item in chips.items():
        locations[item[0]] = generate_domain(item, grid)
    keys = [ key for key in chips.keys() ]
    print(keys)
    csp: CSP[str, List[GridLocation]] = CSP(keys, locations)
    csp.add_constraint(CircuitBoardConstraint(keys))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for chip in solution:
            for grid_location in solution[chip]:
                (row, col) = grid_location
                grid[row][col] = chip
        display_grid(grid)
