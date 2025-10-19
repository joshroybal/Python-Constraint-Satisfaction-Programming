from typing import NamedTuple, List, Dict, Optional, Tuple
from random import choice, shuffle
from string import ascii_uppercase
from csp import CSP, Constraint

Grid = List[List[str]]  # type alias for grids


class GridLocation(NamedTuple):
    row: int
    column: int


def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with random letters
    return [[choice(ascii_uppercase) for c in range(columns)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print('  '.join(row))
        print()


def generate_domain(word: str, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)
    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + length)
            rows: range = range(row, row + length)
            if col + length <= width:
                # left to right
                domain.append([GridLocation(row, c) for c in columns])
                # diagonal towards bottom right
                if row + length <= height:
                    domain.append([GridLocation(r, col + (r - row)) for r in rows])
            if row + length <= height:
                # top to bottom
                domain.append([GridLocation(r, col) for r in rows])
                # diagonal towards bottom left
                if col + 1 - length >= 0:
                    domain.append([GridLocation(r, col - (r - row)) for r in rows])
    return domain


# best so far - sometimes works
class WordSearchConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, words: List[str]) -> None:
        super().__init__(words)
        self.words: List[str] = words

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        # in this version words in the grid are allowed to overlap
        # x = []
        # for word in assignment:
        #     x.append([(i,j) for (i,j) in assignment[word]])

        # for i in range(len(x)):
        #     for j in range(i + 1, len(x)):
        #         words_intersection = set(x[i]) & set(x[j])
        #         if len(words_intersection) > 1:
        #             return False

        d: Dict[Tuple[int, int], str]  = {}
        for word in assignment:
            indices = [(i,j) for (i,j) in assignment[word]]
            for v,k in zip(word,indices):
                if k in d and d[k] != v:
                    return False
                d[k] = v
            #actual = ''.join([d[(i,j)] for (i,j) in assignment[word]])

        return True

if __name__ == "__main__":
    grid: Grid = generate_grid(15, 15)
    #words: List[str] = ["matthew", "joe", "mary", "sarah", "sally"]
    #print(words)
    # Random reverse half the time.
    # Moved random reversal up front because after assignment it breaks the ability to allow
    # overlapping words in WordSearchContraint's satisfied method.
    #words = [ word if choice([True,False]) else word[::-1] for word in words ]
    with open('/usr/dict/words', 'r') as infile:
        words: List[str] = [ line.strip() for line in infile.readlines() ]
    words = [ word for word in words if len(word) <= 15 ]
    shuffle(words)
    words = [ word.upper() for word in words[:15] ]
    clues: List[str] = [word.lower() for word in words]
    shuffle(clues)
    print(clues)
    words = [ word if choice([True,False]) else word[::-1] for word in words ]
    locations: Dict[str, List[List[GridLocation]]] = {}
    for word in words:
        locations[word] = generate_domain(word, grid)
    csp: CSP[str, List[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for word, grid_locations in solution.items():
            for index, letter in enumerate(word):
                (row, col) = (grid_locations[index].row, grid_locations[index].column)
                grid[row][col] = letter
        display_grid(grid)
