# early_risers.py
from typing import List, Dict, Optional, Tuple, Union
from itertools import product
from csp import CSP, Constraint

#def pretty_print(row: List[Union[str, int]]) -> None:
#    print(''.join(['{:20s}'.format(str(s)) for s in row]))

def pretty_print(d: Dict[int, Tuple[str, str, str]]) -> None:
    for k in d:
        print(''.join(['{:20s}'.format(s) for s in [str(k)] + list(d[k])]))

def all_distinct(d: Dict[int, Tuple[str, str, str]]) -> bool:
    checked: List[Tuple[str, str, str]] = []
    for key in d:
        for t in checked:
            for item in d[key]:
                if item in t:
                    return False
        checked.append(d[key])
    return True

def is_girl(child: str) -> bool:
    return child in ['Eleanor', 'Gemma', 'Maggie']

# Save this - this was by far the empirically best processing ordering!
class LogicPuzzleConstraint(Constraint[int, Tuple[str, str, str]]):
    def __init__(self, variables: List[int]) -> None:
        super().__init__(variables)
        self.variables: List[int] = variables

    def satisfied(self, assignment: Dict[int, Tuple[str, str, str]]) -> bool:
        if not all_distinct(assignment):
            return False

        # constrain variables
        if 47 in assignment and '5.00' not in assignment[47]:
            return False
        if 43 in assignment:
            child, time, present = assignment[43]
            if not is_girl(child) or present != 'CD':
                return False

        # constrain domains
        for house_no in assignment:
            t = assignment[house_no]
            if '6.00' in t and 'Sweets' not in t:
                return False
            if 'Eleanor' in t and ('7.00' not in t or 'Computer game' in t):
                return False
            if 'Ben' in t and 'Computer game' in t:
                return False
            if 'Book' in t and '6.30' in t: # check later if needed
                return False
            if 'Maggie' in t and ('5.00' in t or '5.30' in t or 'Jewelry' not in t):
                return False
        
        # search for constraints
        if len(assignment) != 5:
            return True

        EleanorNo: int ; GameNo: int
        BookNo: int ; No630: int
        for house_no in assignment:
            t = assignment[house_no]
            if 'Eleanor' in t:
                EleanorNo = house_no
            if 'Computer game' in t:
                GameNo = house_no
            if 'Book' in t:
                BookNo = house_no
            if '6.30' in t:
                No630 = house_no

        if EleanorNo != 2 + GameNo:
            return False
        if BookNo >= No630:
            return False
        
        return True

if __name__ == '__main__':
    house_nos: List[int] = [43, 45, 47, 49, 51]
    children: List[str] = ['Ben', 'Eleanor', 'Gemma', 'Maggie', 'Matthew']
    times: List[str] = ['5.00', '5.30', '6.00', '6.30', '7.00']
    presents: List[str] = ['Book', 'CD', 'Computer game', 'Jewelry', 'Sweets']
    domains: Dict[int, List[Tuple[str, str,str]]] = { house_no: list(product(children, times, presents)) for house_no in house_nos }
    csp: CSP[int, Tuple[str, str, str]] = CSP(house_nos, domains)
    csp.add_constraint(LogicPuzzleConstraint(house_nos))
    solution: Optional[Dict[int, Tuple[str, str, str]]] = csp.backtracking_search()

    if solution is None:
        print('No solution found!')
    else:
        print('Solution found!')
        #print(solution)
        pretty_print(solution)
