"""
Constraint for checking the type and structure of values
"""

from typing import Union
from types import FunctionType

class SimpleConstraint:
    """
    `SimpleConstraint` class. Constraint that only specifies type
    """

    def __init__(self, constraint: type) -> None:
        self.constraint = constraint
    
    def is_constraint_valid(self) -> bool:
        return SimpleConstraint.is_simple_constraint(self.constraint)
    
    @staticmethod
    def is_simple_constraint(constraint) -> bool:
        return type(constraint) == type

    def validate(self, value) -> bool:
        return SimpleConstraint.static_validate(self.constraint, value)
    
    @staticmethod
    def static_validate(constraint: type, value) -> bool:
        """
        validate value
        """
        # check whether is constraint valid
        if not SimpleConstraint.is_simple_constraint(constraint):
            return False
        
        return type(value) == constraint
        

class DictConstraint:
    """
    `DictConstraint` class. Constraint for checking structure and datatype of dictionary.
    """

    def __init__(self, structure: dict, accept_excess = True, accept_scarcity = False) -> None:
        self.structure = structure
        self.accept_excess = accept_excess
        self.accept_scarcity = accept_scarcity
    
    def is_constraint_valid(self) -> bool:
        return DictConstraint.is_valid_dt_constraint(self.structure)

    @staticmethod
    def is_valid_dt_constraint(structure: dict) -> bool:
        """
        is dictionary constraint valid
        """

        if type(structure) != dict:
            return False

        for key in structure:
            if type(key) == type: # only accept literal value
                return False
            
            value_c = structure[key]
            if type(value_c) == list:
                if not ListLikeConstraint.is_valid_lk_constraint(value_c):
                    return False
            elif type(value_c) == dict :
                if not DictConstraint.is_valid_dt_constraint(value_c):
                    return False
            elif (type(value_c) != type):
                return False
        return True
    
    def validate(self, value):
        return DictConstraint.static_validate(self.structure, value, self.accept_excess, self.accept_scarcity)

    @staticmethod
    def static_validate(structure:dict, value: dict, accept_excess = True, accept_scarcity = False) -> bool:
        """
        validate value
        """

        if not DictConstraint.is_valid_dt_constraint(structure):
            return False
        
        if type(value) != dict:
            return False

        value_keys = list(value.keys())
        for key in structure:
            if key in value_keys: # value contains key required
                value_keys.remove(key) # remove checked key. if there still have keys after checking, is_excess = true

                # Check
                if SimpleConstraint.is_simple_constraint(structure[key]):
                    if not SimpleConstraint.static_validate(structure[key], value[key]):
                        return False
                elif DictConstraint.is_valid_dt_constraint(structure[key]):
                    if not DictConstraint.static_validate(structure[key], value[key]):
                        return False
                elif ListLikeConstraint.is_valid_lk_constraint(structure[key]):
                    if not ListLikeConstraint.static_validate(structure[key], value[key]):
                        return False
                elif Or.is_or_constraint(structure[key]):
                    if not Or.validate(structure[key], value[key]):
                        return False
                    
            else: # value do not contains key required
                if not accept_scarcity:
                    return False
        
        return not(bool(len(value_keys)) and not accept_excess)

class ListLikeConstraint:
    """
    `ListLikeConstraint` class. Constraint that specifies structure of a list or tuple.
    
    structure (constraint) can be very flexible.
    Example of structure:
    [int, int, int]:
        [1,2,3] => accepted
        [1,2,3,4] => not accepted
        [1,2] => not accepted
        ["LOL"] => not accepted
    [Countless(int)]:
        [1] => accepted
        [1, 2, 3,4 ,5 , 6, 7, 8] => accepted
        ["moo"] => not accepted
    [Multiple(int, 3)] (same as [int, int, int]):
        [1,2,3] => accepted
        [1,2,3,4] => not accepted
        [1,2] => not accepted
        ["LOL"] => not accepted
    [Countless((int, int))]:
        [(1,2),(445,65)] => accepted
        [65] => not accepted
    """

    class Countless:
        def __init__(self, type: type, at_least: int = 1) -> None:
            self.type = type
            self.at_least = at_least
    
        def __repr__(self) -> str:
            return f"Countless({self.type}, at least {self.at_least} elements)"
        
        def validate(self, value):
            if SimpleConstraint.is_simple_constraint(self.type):
                return SimpleConstraint.static_validate(self.type, value)
            elif ListLikeConstraint.is_valid_lk_constraint(self.type):
                return ListLikeConstraint.static_validate(self.type, value)
            elif DictConstraint.is_valid_dt_constraint(self.type):
                return DictConstraint.static_validate(self.type, value)

    class Multiple:
        def __init__(self, type: type, count: int) -> None:
            self.type = type
            self.count = count

        def __repr__(self) -> str:
            return f"Multiple({self.type}, {self.count})"

    def __init__(self, structure: Union[list, tuple]) -> None:
        self.structure = structure
    
    def is_constraint_valid(self) -> bool:
        return ListLikeConstraint.is_valid_lk_constraint(self.structure)

    @staticmethod
    def is_valid_lk_constraint(structure: Union[list, tuple]) -> bool:
        """
        is list-like constraint valid
        """

        if type(structure) not in [list, tuple]:
           return False

        for c in structure:
            if type(c) in [list, tuple]: # if element is another list-like constraint
                if not ListLikeConstraint.is_valid_lk_constraint(c):
                    return False
            elif type(c) == dict:
                if not DictConstraint.is_valid_dt_constraint(c):
                    return False
            elif type(c) not in [ type, ListLikeConstraint.Countless, ListLikeConstraint.Multiple ]: # acceptable type of elements in structure
                return False
        return True

    def validate(self, value) -> bool:
        """
        Validate value
        """
        return ListLikeConstraint.static_validate(self.structure, value)
    
    @staticmethod
    def static_validate(structure: Union[list, tuple], value) -> bool:
        """
        Validate whether value follows the structure
        """
        s_structure = ListLikeConstraint.simplify_constraint(structure)
        if s_structure == None:
            return False
        
        if type(value) not in [list, tuple]:
            return False
        
        offset = 0
        for i, c in enumerate(s_structure):
            value_i = i + offset

            if value_i >= len(value):
                return False

            if SimpleConstraint.is_simple_constraint(c):
                if not SimpleConstraint.static_validate(c,value[value_i]):
                    return False
            elif ListLikeConstraint.is_valid_lk_constraint(c):
                if not ListLikeConstraint.static_validate(c,value[value_i]):
                    return False
            elif DictConstraint.is_valid_dt_constraint(c):
                if not DictConstraint.static_validate(c,value[value_i]):
                    return False
            elif Or.is_or_constraint(c):
                if not Or.validate(c, value[value_i]):
                    return False
            elif type(c) == ListLikeConstraint.Countless:
                same_type_count = 0
                while True:
                    # check type
                    if value_i >= len(value) or not c.validate(value[value_i]):
                        if same_type_count < c.at_least:
                            return False
                        else:
                            offset -= 1
                            break
                    else:
                        same_type_count += 1
                        offset += 1
                        value_i = i + offset

        
        if offset + len(s_structure) != len(value):
            return False
        return True

    @staticmethod
    def simplify_constraint(structure: Union[list, tuple]) -> Union[None, list, tuple]:
        """
        Expands `Multiple` class into types ([Multiple(int, 3)] => [int, int, int])

        Merge `Countless` class with types ([Countless(int, at_least = 1), int, int] => [Countless(int, at_least = 3)])
        Merge `Countless` class with adjecent `Countless class ([Countless(int, at_least=1), Countless(int, at_least=3)] => [Countless(int, at_least = 4)])

        Note: function do not simplify recursively. Nested lf-constraint will not be simplified
        """
        if not ListLikeConstraint.is_valid_lk_constraint(structure):
            return None
        
        structure_type = type(structure)

        def expand_mt(structure):
            """
            Expand `Multiple` class in a structure (constraint)
            """
            e = []
            for c in structure:
                if type(c) == ListLikeConstraint.Multiple:
                    for _ in range(c.count):
                        e.append(c.type)
                else:
                    e.append(c)
            return e
        
        def get_ct_group_info(structure):
            """
            Group `Countless` class. Assume there is no `Multiple` class.

            returns list of (group_start, group_end, new_countless)

            Example:
            [int, Countless(int, at_least=1), int, int, str] => [(0, 3, Countless(int, 4))]
            [int, Countless(int, at_least=1), str, int, Countless(int, at_least=2)] => [(0, 1, Countless(int, at_least=2)), (3, 4, Countless(int, at_least=3))]
            """

            result = []
            ct_indexes = [ i for i, c in enumerate(structure) if type(c) == ListLikeConstraint.Countless]
            for ct_i in ct_indexes:
                new_countless = ListLikeConstraint.Countless(structure[ct_i].type, structure[ct_i].at_least)
                group_start = 0
                group_end = len(structure) - 1
                # find the group_start
                for s_i in range(ct_i - 1, -1, -1):
                    c = structure[s_i]
                    if c == new_countless.type: # found type that is same as Countless' type
                        new_countless.at_least += 1
                    else: # found other types (no good no good)
                        group_start = s_i + 1
                        break
                
                # find the group_end
                for s_i in range(ct_i+1, len(structure)):
                    c = structure[s_i]
                    if type(c) == ListLikeConstraint.Countless and c.type == new_countless.type: # found adjecent countless with same type
                        new_countless.at_least += c.at_least
                        ct_indexes.remove(s_i) # remove the Countless that will be grouped as it already grouped with this group
                    elif c ==new_countless.type: # found type that is same as Countless' type
                        new_countless.at_least += 1
                    else: # found other types (no good no good)
                        group_end = s_i - 1
                        break

                result.append((group_start, group_end, new_countless))
            return result

        expanded = expand_mt(structure)
        ct_groups = get_ct_group_info(expanded)
        new_structure = []
        last_end = 0
        for start, end, ct in ct_groups:
            new_structure = [ *new_structure, *expanded[last_end: start], ct ]
            last_end = end + 1
        new_structure = [ *new_structure, *expanded[last_end:] ]
        return structure_type(new_structure)
        
        
class Or:
    """
    `Or` class. A `Union` constraint
    """

    def __init__(self, *constraint) -> None:
        self.constraint_list = constraint

    @staticmethod
    def is_or_constraint(constraint) -> bool:
        return type(constraint) == Or
    
    def validate(self, value) -> bool:
        for c in self.constraint_list:
            if SimpleConstraint.is_simple_constraint(c):
                if SimpleConstraint.static_validate(c,value):
                    return True
            elif ListLikeConstraint.is_valid_lk_constraint(c):
                if ListLikeConstraint.static_validate(c,value):
                    return True
            elif DictConstraint.is_valid_dt_constraint(c):
                if DictConstraint.static_validate(c,value):
                    return True
        return False
    
    @staticmethod
    def static_validate(constraint, value) -> bool:
        if not Or.is_or_constraint(constraint):
            return False
        
        return constraint.validate(value)


