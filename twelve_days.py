# trump_cards.py
import sys
from itertools import product
from typing import List, Dict, Optional, Tuple
from csp import CSP, Constraint

def pretty_print(row: List[str]) -> None:
    print('|' + '|'.join(['{:18s}'.format(s) for s in row]) + '|')
    #print(''.join(['{:20s}'.format(s) for s in row]))

def all_distinct(d: Dict[int, Tuple[str, int]]) -> bool:
    vals: List[Tuple[str, int]] = [d[k] for k in d]
    i: int ; j : int
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if not set(vals[i]).isdisjoint(vals[j]):
                return False
    return True

def is_boy(name: str) -> bool:
    return name in ['john', 'luke', 'mark', 'matthew', 'nicholas', 'noel']

def is_girl(name: str) -> bool:
    return name in ['angela', 'carole', 'holly', 'ivy', 'joy', 'mary']

def is_even(n: int) -> bool:
    return n % 2 == 0

def is_odd(n: int) -> bool:
    return n % 2 == 1

# partial pruning to try to avoid combinatorial explosion
# kind of half-baked arc satisfaction
def restrict_domains(domains):
    # 1.
    for i in domains:
        domains[i] = [(n,d) for (n,d) in domains[i] if not (is_boy(n) and d == 10)]
    domains[7] = [(n,d) for (n,d) in domains[7] if is_girl(n)]
    # 2.
    domains[3] = [(n,d) for (n,d) in domains[3] if n != 'nicholas' and d != 12 and is_even(d) and is_boy(n)]
    for i in domains:
        domains[i] = [(n,d) for (n,d) in domains[i] if not (n == 'ivy' and d != 5)]
    # 3.
    for i in domains:
        domains[i] = [(n,d) for (n,d) in domains[i] if not (d == 12 and is_boy(n))]
        domains[i] = [(n,d) for (n,d) in domains[i] if not (n == 'john' and d > 5)]
    domains[1] = [(n,d) for (n,d) in domains[1] if n != 'john']
    domains[12] = [(n,d) for (n,d) in domains[12] if d != 12]
    # 4.
    domains[1] = [(n,d) for (n,d) in domains[1] if n != 'carole' and d != 1 and d != 12]
    # 5.
    domains[9] = [(n,d) for (n,d) in domains[9] if n == 'matthew']
    for i in domains:
        if i == 9: continue
        domains[i] = [(n,d) for (n,d) in domains[i] if n != 'matthew']
                      
    for n in domains:
        print(len(domains[n]))
    return domains

class LogicPuzzleConstraint(Constraint[int, Tuple[str,int]]):
    def __init__(self, house_nos: List[int]) -> None:
        super().__init__(house_nos)
        self.house_nos: List[int] = house_nos

    def satisfied(self, assignment: Dict[int, Tuple[str, int]]) -> bool:
        if not all_distinct(assignment):
            return False
        if len(assignment) < 12:
            return True
        #names: List[str] = [ 'john', 'luke', 'mark', 'matthew', 'nicholas', 'noel', 'angela', 'carole', 'holly', 'ivy', 'joy', 'mary' ]
        # 2.
        nicholas_date: int ; three_date: int
        ivy_house: int ; nicholas_house: int
        for house in assignment:
            name, date = assignment[house]
            if house == 3:
                three_date = date
            if name == 'nicholas':
                nicholas_date = date
                nicholas_house = house
            if name == 'ivy':
                ivy_house = house
        #print(three_date, nicholas_date)
        if nicholas_date != three_date + 1: return False
        if abs(nicholas_house - ivy_house) != 1: return False
        
        return True

if __name__ == "__main__":
    house_nos: List[int] = list(range(1, 13))
    names: List[str] = [ 'john', 'luke', 'mark', 'matthew', 'nicholas', 'noel', 'angela', 'carole', 'holly', 'ivy', 'joy', 'mary' ]
    dates: List[int] = list(range(1, 13))
    domains: Dict[int, List[Tuple[str, int]]] = { house_no: [t for t in product(names, dates)] for house_no in house_nos }
    # normally not needed to avoid combinatorial explosion in these toy exs.
    #print(domains)
    #print()
    domains = restrict_domains(domains)
    #print(domains)
    quit()
    #print()
    csp: CSP[int, Tuple[str, int]] = CSP(house_nos, domains)
    csp.add_constraint(LogicPuzzleConstraint(house_nos))
    solution: Optional[Dict[int, Tuple[str, int]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print("Solution found!")
        print(solution)
        #headers: List[str] = ["House Nos.", "Names", "Dates"]
        #pretty_print(headers)
        #for row in solution:
        #    pretty_print(solution[row])
