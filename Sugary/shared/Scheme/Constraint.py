"""
Provides Classes for storing constraints in Scheme
"""

from typing import Union

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
        return SimpleConstraint.validate(self.constraint, value)
    
    @staticmethod
    def validate(constraint: type, value) -> bool:
        """
        validate value
        """
        # check whether is constraint valid
        if not SimpleConstraint.is_simple_constraint(constraint):
            return False
        
        return type(value) == constraint
        

class DictConstraint:
    """
    `DictConstraint` class. Constraint for dictionary
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
            if type(value_c) in [list, tuple]: # if value is another list-like constraint
                if not ListLikeConstraint.is_valid_lk_constraint(value_c):
                    return False
                elif type(value_c) == dict:
                    if not DictConstraint.is_valid_dt_constraint(value_c):
                        return False
                elif type(value_c) == type:
                    return False
        return True
    
    def validate(self, value):
        return DictConstraint.validate(self.structure, value, self.accept_excess, self.accept_scarcity)

    @staticmethod
    def validate(structure:dict, value: dict, accept_excess = True, accept_scarcity = False) -> bool:
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
                    if not SimpleConstraint.validate(structure[key], value[key]):
                        return False
                    continue
                elif DictConstraint.is_valid_dt_constraint(structure[key]):
                    if not DictConstraint.validate(structure[key], value[key]):
                        return False
                    continue
                elif ListLikeConstraint.is_valid_lk_constraint(structure[key]):
                    if not ListLikeConstraint.validate(structure[key], value[key]):
                        return False
                    continue
                else:
                    return False
                    
            else: # value do not contains key required
                if not accept_scarcity:
                    return False
        
        return not(bool(len(value_keys)) and not accept_excess)
        

class ListLikeConstraint:
    """
    `ListLikeConstraint` class. Constraint that specifies structure of a list or tuple
    """

    class Countless:
        def __init__(self, type: type, at_least: int = 1) -> None:
            self.type = type
            self.at_least = at_least
    
        def __repr__(self) -> str:
            return f"Countless({self.type}, at least {self.at_least} elements)"


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

    # TODO
    def validate(self, value) -> bool:
        """
        Validate value
        """
        return
    
    # TODO
    @staticmethod
    def validate(structure: Union[list, tuple], value) -> bool:
        pass

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

        # expand multiple
        def expand_mt(structure):
            e = []
            for c in structure:
                if type(c) == ListLikeConstraint.Multiple:
                    for _ in range(c.count):
                        e.append(c.type)
                else:
                    e.append(c)
            return e
        
        e = expand_mt(structure)
        
        # Merge Countless class with types
        def merge_ct_with_types(structure: list):
            s = []
            i_from = 0 # keep track on what we copied to which index in `expanded` list
            ct_indexes = [ i for i in range(len(structure)) if type(structure[i]) == ListLikeConstraint.Countless]
            for ct_i in ct_indexes:
                expected_type = structure[ct_i].type # current Countless's type
                new_ct = ListLikeConstraint.Countless(expected_type, structure[ct_i].at_least)
                i_to = i_from
                new_i_from = i_from

                for j in range(ct_i - 1, -1, -1): # loop from the index before Countless class to the begining
                    if structure[j] == expected_type:
                        new_ct.at_least += 1
                    else:
                        i_to = j + 1
                        break
                    if j == 0:
                        i_to = j 
                        break
                        
                for j in range(ct_i + 1, len(structure)):
                    if structure[j] == expected_type:
                        new_ct.at_least += 1
                    else:
                        new_i_from = j
                        break
                    if j == len(structure) - 1:
                        new_i_from = j
                        break
                        
                s = [ *s , *structure[i_from: i_to], new_ct ]
                i_from = new_i_from
            return [ *s, *structure[i_from:] ]
        
        s1 = merge_ct_with_types(e)
            
        def merge_cts(structure:list):
            s = []
            recent_countless: Union[ListLikeConstraint.Countless, None] = None 
            new_countless: Union[ListLikeConstraint.Countless, None] = None
            for i in structure:
                if type(i) != ListLikeConstraint.Countless:
                    if new_countless != None:
                        s.append(new_countless)
                        new_countless = None
                    recent_countless = None
                    s.append(i)
                else:
                    # i is a Countless instance
                    if recent_countless != None:
                        if recent_countless.type == i.type:
                            if new_countless == None:
                                new_countless = ListLikeConstraint.Countless(i.type, recent_countless.at_least + i.at_least)
                            else:
                                new_countless.at_least += i.at_least
                        else:
                            if new_countless != None:
                                s.append(new_countless)
                                new_countless = None
                            else:
                                s.append(recent_countless)
                                recent_countless = None
                                s.append(i)
                    else:
                        recent_countless = i
            return s
        
        return structure_type(merge_cts(s1))


class AdvanceConstraint:
    """
    `AdvanceConstraint` class. Beyond just types.
    """