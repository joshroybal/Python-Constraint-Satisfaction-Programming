# trump_cards.py
import sys
from itertools import product
from typing import List, Dict, Optional
from csp import CSP, Constraint

def pretty_print(row: List[str]) -> None:
    print('|' + '|'.join(['{:18s}'.format(s) for s in row]) + '|')
    #print(''.join(['{:20s}'.format(s) for s in row]))

def all_distinct(d: Dict[int, List[str]]) -> bool:
    vals: List[List[str]] = [d[k] for k in d]
    i: int ; j : int
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if not set(vals[i]).isdisjoint(vals[j]):
                return False
    return True

class LogicPuzzleConstraint(Constraint[int, List[str]]):
    def __init__(self, rows: List[int]) -> None:
        super().__init__(rows)
        self.rows: List[int] = rows

    def satisfied(self, assignment: Dict[int, List[str]]) -> bool:
        # Prolog style mnemonic
        # [_,Spencer,Kaos,_]
        # [_,_,_,Dickens characters]
        # [_,Constable,_,Polar Bears]
        # [_,_,_,_]
        # [_,_,_,_]
        men: List[str] = ["Bertram", "Jonathan"]
        women: List[str] = ["Fenella", "Pauline", "Samantha"]
        if not all_distinct(assignment):
            return False
        if "Spencer" not in assignment[1] or "Kaos" not in assignment[1]:
            return False
        if len(assignment) == 2:
            if "Dickens characters" not in assignment[2]:
                return False
            if assignment[1][0] in men and assignment[2][0] in women:
                return False
            if assignment[1][0] in women and assignment[2][0] in men:
                return False            
        if len(assignment) == 3:
            if "Constable" not in assignment[3] or "Polar bears" not in assignment[3]:
                return False
            # computer engineers prefer NAND
            #if not ("Constable" in assignment[3] and "Polar bears" in assignment[3]):
            #    return False
        for row in assignment:
            vals: List[str] = assignment[row]
            if "Pauline" in vals and "Luv2Luv" not in vals:
                return False
            if "Samantha" in vals and "Reynolds" not in vals:
                return False
            if "Fenella" in vals and "Narcissus" in vals:
                return False
            if "Narcissus" in vals and "Dinosaurs" not in vals:
                return False
            if "Munnings" in vals and vals[0] in men:
                return False
            if "Jonathan" in vals and "Comedy caricatures" not in vals:
                return False
            if "Jonathan" in vals and "Obelisk" in vals:
                return False
            if "Obelisk" in vals and "Santa's elves" in vals:
                return False
            if "Jonathan" in vals and "Leighton" in vals:
                return False
            if "Obelisk" in vals and "Leighton" in vals:
                return False
        return True

if __name__ == "__main__":
    first_names: List[str] = [ "Bertram", "Fenella", "Jonathan", "Pauline", "Samantha" ]
    surnames: List[str] = [ "Constable", "Leighton", "Munnings", "Reynolds", "Spencer" ]
    publisher: List[str] = ["Kaos", "Luv2Luv", "Lyndon", "Narcissus", "Obelisk" ]
    series: List[str] = [ "Comedy caricatures", "Dickens characters", "Dinosaurs", "Polar bears", "Santa's elves" ]
    row_nos: List[int] = [ 1, 2, 3, 4, 5 ]
    columns: List[List[str]] = [ list(col) for col in product(first_names, surnames, publisher, series) ]
    #print(columns)
    domains: Dict[int, List[List[str]]] = { i: columns for i in row_nos }
    csp: CSP[int, List[str]] = CSP(row_nos, domains)
    csp.add_constraint(LogicPuzzleConstraint(row_nos))
    solution: Optional[Dict[int, List[str]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print("Solution found!")
        headers: List[str] = ["First name", "Surname", "Publisher", "Series"]
        pretty_print(headers)
        for row in solution:
            pretty_print(solution[row])
