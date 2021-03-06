"""A python module that provides a simple way to validate value through constraint.

There are 5 basic constraint:
1. type constraint
2. dictionary constraint
3. list-like constraint
4. 'or' constraint
5. 'check' constraint

and each constraint can be used to validate value using these classes:
1. TypeConstraint (for validating value using a type constraint)
2. DictConstraint (for validating dictionaries using a dictionary constraint)
3. ListLikeConstraint (for validating tuples or lists using a list-like constraint)
4. Or (for validating values using constraint that is a "union" of all basic constraint)
5. Check (for validating values according to user's desire)

A type constraint checks for value's type. 
A dictionary constraint checks for dictionary's structure (how key value pair should be).
A list-like constraint checks for structure of a list or a tuple.
An 'or' constraint let user to combines constraint. 
A 'check' constraint let user defines how to validate value.

Please read the docstring of each constraint's classes for furthur information.
"""

from typing import Union
from types import FunctionType


class InvalidConstraintError:

    def __init__(self, constraint, constraint_class: type) -> None:
        self.constraint = constraint
        self.constraint_class = constraint_class
    
    def get_error(self) -> str:
        return f"The constraint, '{self.constraint}', is not a valid '{self.constraint_class.__name__}'"
    
    def __repr__(self) -> str:
        return f"InvalidConstraintError({self.get_error()})"

class UnsatisfiedError:

    def __init__(self, err) -> None:
        self.err = err
    
    def __repr__(self) -> str:
        return f"UnsatisfiedError({self.err})"
    
class TypeConstraint:
    """A class that checks value's type using constraint

    Create an instance by passing in a type constraint. A type constraint is basically a type (`str`, `int`, and etc.)
    The instance can be used to validate value by calling `validate` method.
    Value said to be valid when the value's type is equal to the type constraint (satisfies the constraint)

    Attribute:
    -----
    constraint : type
        The type constraint

    Static Methods:
    -----
    is_valid_type_constraint(constraint: any) -> bool
        Check whether the constraint is a valid type constraint
    static_validate(constraint: type, value: any) -> Union[bool, InvalidConstraintError, UnsatisfiedError]
        Validate the value using the constraint

    Methods:
    -----
    is_constraint_valid() -> bool
        Check whether the instance's constraint is a valid type constraint.
    validate(value: any) -> Union[bool, InvalidConstraintError, UnsatisfiedError]
        Validate the value using the instance's constraint.
    """

    def __init__(self, constraint: type) -> None:
        self.constraint = constraint

    def is_constraint_valid(self) -> bool:
        """Check whether the instance's constraint is a valid type constraint

        Returns:
            bool: True if the instance's constraint is valid, else False
        """

        return TypeConstraint.is_valid_type_constraint(self.constraint)

    @staticmethod
    def is_valid_type_constraint(constraint) -> bool:
        """Check whether the constraint is a valid type constraint

        Args:
            constraint (any): constraint to be checked

        Returns:
            bool: True if the constraint is valid, else False
        """

        return type(constraint) == type

    def validate(self, value) -> Union[bool, InvalidConstraintError, UnsatisfiedError]:
        """Validate the value using the instance's constraint

        Args:
            value (any): value to be validated

        Returns:
            Union[bool, InvalidConstraintError, UnsatisfiedError]: if value is accepted, return False, else return an instance of error class (InvalidConstraintError or UnsatisfiedError)
        """

        return TypeConstraint.static_validate(self.constraint, value)

    @staticmethod
    def static_validate(constraint: type, value) -> Union[bool, InvalidConstraintError, UnsatisfiedError]:
        """Validate the value using the constraint

        Args:
            constraint (type): the constraint used
            value (any): value to be validated

        Returns:
            Union[bool, InvalidConstraintError, UnsatisfiedError]: if value is accepted, return False, else return an instance of error class (InvalidConstraintError or UnsatisfiedError)
        """

        # check whether is constraint valid
        if not TypeConstraint.is_valid_type_constraint(constraint):
            return InvalidConstraintError(constraint, TypeConstraint)

        return type(value) != constraint and UnsatisfiedError(f"Expecting the value's type to be '{constraint.__name__}' but the type of value '{value}' is '{type(value).__name__}'")


class DictConstraint:
    """A class that checks dictionaries using dictionary constraint

    Create an instance by passing in an dictionary constraint, and specify accept_excess and accept_scarcity.

    Dictionary constraint is basically a dictionary.
    Example of a dictionary constraint:
    ```
    example_constraint = {
        "type_constraint": bool,
        "dict_constraint": {
            "key": int
        },
        "list_like_constraint": [int, int, int]
        "or_constraint": Or(int, str)
        "check_constraint": Check(func)
    }
    ```
    A Dictionary constraint's key must not be a type.
    Its value must be either a type constraint, dictionary constraint, list-like constraint, 'or' constraint, or 'check' constraint.

    Validation will be carry out according to key. `value[key]` will be validated using the `constraint[key]`.
    For instances,
    ```
    value = {
        "type_constraint": False,
        "or_constraint": 1
    }
    ```
    When `value` is validated using `example_constraint`, `value["type_constraint"]` will be validated by the `example_constraint["type_constraint"]`.
    Same goes to `value["or_constraint"]`.
    Read the `Attributes` section for `accept_excess` and `accept_scarcity`.

    Attributes:
    -----
    constraint : dict
        A dictionary constraint
    accept_excess : bool
        Accept dictionary to be validated contains key that the dictionary constraint doesn't contains.
        It makes the `validate` returns false if dictionary contains key that the constraint doesn't containts and accept_excess = False.
    accept_scarcity : bool
        Accept dictionary to be validated does not contain key that the dictionary constraint has.
        It makes the `validate` returns false if dictionary does not contain key that the constraint has and accept_scarcity = False.

    Static method:
    -----
    is_valid_dt_constraint(constraint: any) -> bool
        Check whether the constraint is a valid dictionary constraint.
    static_validate(constraint: dict, value: any, accept_excess = True, accept_scarcity = False) -> Union[bool, InvalidConstraintError, UnsatisfiedError]
        Validate the value using the constraint

    Method:
    -----
    is_constraint_valid(self) -> bool
        Check whether the instance's constraint is a valid dictionary constraint.
    validate(value: any) -> Union[bool, InvalidConstraintError, UnsatisfiedError]
        Validate the value using the instance's constraint
    """

    def __init__(
        self, constraint: dict, accept_excess=True, accept_scarcity=False
    ) -> None:
        self.constraint = constraint
        self.accept_excess = accept_excess
        self.accept_scarcity = accept_scarcity

    def is_constraint_valid(self) -> bool:
        """Check whether the instance's constraint is a valid dictionary constraint.

        A dictionary cosntraint must be:
        1. A dictionary
        2. The keys must not be a type (int class, str class)
        3. The value must be either a type constraint, dictionary constraint, list-like constraint, 'or' constraint, or 'check' constraint.

        Returns:
            bool: whether the instance's constraint is a valid dictionary constraint
        """

        return DictConstraint.is_valid_dt_constraint(self.constraint)

    @staticmethod
    def is_valid_dt_constraint(constraint) -> bool:
        """Check whether the constraint is a valid dictionary constraint.

        A dictionary cosntraint must be:
        1. A dictionary
        2. The keys must not be a type (int class, str class)
        3. The value must be either a type constraint, dictionary constraint, list-like constraint, 'or' constraint, or 'check' constraint.

        Args:
            constraint (any): constraint to be checked

        Returns:
            bool: True if the constraint is a valid constraint, else False
        """

        if type(constraint) != dict:
            return False

        for key in constraint:
            if type(key) == type:  # only accept literal value
                return False

            value_c = constraint[key]
            if get_constraint_class(
                value_c
            ):  # if there is a class for the constraint, it is a valid constraint
                continue
            else:
                return False
        return True

    def validate(self, value) -> Union[bool, InvalidConstraintError, UnsatisfiedError]:
        """Validate the value using the instance's constraint

        `value[key]` will be validated using the `constraint[key]`.
        Read Documentation of `DictConstraint` class for example.
        Always return False if the instance's constraint is not a valid dictionary constraint.

        Args:
            value (any): value to be validated

        Returns:
            Union[bool, InvalidConstraintError, UnsatisfiedError]: if no complain, return False, else returns error.
        """

        return DictConstraint.static_validate(
            self.constraint, value, self.accept_excess, self.accept_scarcity
        )

    @staticmethod
    def static_validate(
        constraint: dict, value: dict, accept_excess=True, accept_scarcity=False
    ) -> Union[bool, InvalidConstraintError, UnsatisfiedError]:
        """Validate the value using the instance's constraint

        `value[key]` will be validated using the `constraint[key]`.
        Read Documentation of `DictConstraint` class for example.
        Always return False if the instance's constraint is not a valid dictionary constraint.

        Args:
            constraint (dict): dictionary constraint used
            value (any): value to be validated
            accept_excess: accept value to have extra key value pair than constraint
            accept_scarcity: accept value doesn't contains key in constraint

        Returns:
            Union[bool, InvalidConstraintError, UnsatisfiedError]: if no complain, return False, else returns error.
        """

        if not DictConstraint.is_valid_dt_constraint(constraint):
            return InvalidConstraintError(constraint, DictConstraint)

        if type(value) != dict:
            return UnsatisfiedError(f"Expecting the value to be a 'dict' but the type of value '{value}' is '{type(value).__name__}'")

        value_keys = list(value.keys())
        for key in constraint:
            if key in value_keys:  # value contains key required
                value_keys.remove(
                    key
                )  # remove checked key. if there still have keys after checking, is_excess = true

                # Check
                if TypeConstraint.is_valid_type_constraint(constraint[key]):
                    err = TypeConstraint.static_validate(constraint[key], value[key])
                    if err:
                        return err
                elif DictConstraint.is_valid_dt_constraint(constraint[key]):
                    err = DictConstraint.static_validate(constraint[key], value[key])
                    if err:
                        return err
                elif ListLikeConstraint.is_valid_lk_constraint(constraint[key]):
                    err = ListLikeConstraint.static_validate(
                        constraint[key], value[key]
                    )
                    if err:
                        return err
                elif Or.is_valid_or_constraint(constraint[key]):
                    err = Or.validate(constraint[key], value[key])
                    if err:
                        return err
                elif Check.is_valid_check_constraint(constraint[key]):
                    err = Check.validate(constraint[key], value[key])
                    if err:
                        return err

            else:  # value do not contains key required
                if not accept_scarcity:
                    return UnsatisfiedError(f"The value '{value}' do not contains '{key}'")

        return (bool(len(value_keys)) and not accept_excess) and UnsatisfiedError(f"The value '{value}' contains extra keys")


class ListLikeConstraint:
    """A class that checks list-like values using list-like constraint

    A list-like values can be a list or a tuple.
    A list-like constraint is basically a list or a tuple.
    A list-like constraint's element must be either:
        1. a type constraint
        2. dictionary constraint
        3. list-like constraint
        4. 'or' constraint
        5. 'check' constraint
        6. instance of `Countless` class
        7. instance of `Multiple` class

    Validation of value using constraint occurs element by element.
    Element of constraint is used to validate element of value.
    Example of how list-like constraint validate value:
        [int, int, int]:
            [1,2,3] => accepted
            [1,2,3,4] => not accepted
            [1,2] => not accepted
            ["LOL"] => not accepted
            (1,2,3) => not accepted
        [Countless(int)]:
            [1] => accepted
            [1, 2, 3, 4 ,5 , 6, 7, 8] => accepted
            ["moo"] => not accepted
            [] => not accepted
        [Multiple(int, 3)] (same as [int, int, int]):
            [1,2,3] => accepted
            [1,2,3,4] => not accepted
            [1,2] => not accepted
            ["LOL"] => not accepted
        [Countless((int, int))]:
            [(1,2),(445,65)] => accepted
            [65] => not accepted

    Attribute:
    -----
    constraint : list
        The list-like constraint

    Static Methods:
    -----
    is_valid_lk_constraint(constraint: any) -> bool
        Check whether the constraint is a valid list-like constraint
    static_validate(constraint: Union[list, tuple], value: any) -> Union[bool, UnsatisfiedError, InvalidConstraintError]
        Validate the value using the constraint
    simplify_constraint(constraint: Union[list, tuple]) -> Union[None, list, tuple]
        Returns simplified version of list-like constraint. Returns None if the constraint given is invalid.

    Subclass:
    -----
        Countless
            A class that represents countless constraints in a list-like constraint.
        Multiple
            A class that represents multiple constraints in a list-like constraint.

    Methods:
    -----
    is_constraint_valid() -> bool
        Check whether the instance's constraint is a valid list-like constraint.
    validate(value: any) -> Union[bool, UnsatisfiedError, InvalidConstraintError]
        Validate the value using the instance's list-like constraint.

    """

    class Countless:
        """A class that represents countless constraint in a list-like constraint.

        Attributes:
        -----
        constraint
            it can only be a
                1. a type constraint
                2. dictionary constraint
                3. list-like constraint
                4. 'or' constraint
                5. 'check' constraint
        at_lease : int
            at least how many element in the list (value) that satisfies constraint so it is considered accepted.

        Method:
        -----
        is_constraint_valid() -> bool
            Check the validity of the self.constraint
        validate(value: any) -> bool
            Return the result of validation.
            If the constraint is not any kind of constraint, returns False.
        """

        def __init__(self, constraint, at_least: int = 1) -> None:
            self.constraint = constraint
            self.at_least = at_least

        def __repr__(self) -> str:
            return f"Countless({self.constraint}, at least {self.at_least} elements)"

        def is_constraint_valid(self) -> bool:
            """Check the validity of the self.constraint

            self.constraint can only be:
                1. a type constraint
                2. dictionary constraint
                3. list-like constraint
                4. 'or' constraint
                5. 'check' constraint

            Returns:
                bool: whether self.constraint is valid
            """

            return not not get_constraint_class(self.constraint)

        def validate(self, value) -> bool:
            """Returns the result of validation based on type of constraint

            If the constraint is not any kind of constraint, returns False.

            Args:
                value (any): value to be validated

            Returns:
                bool: result of validation
            """

            if TypeConstraint.is_valid_type_constraint(self.constraint):
                return not TypeConstraint.static_validate(self.constraint, value)
            elif ListLikeConstraint.is_valid_lk_constraint(self.constraint):
                return not ListLikeConstraint.static_validate(self.constraint, value)
            elif DictConstraint.is_valid_dt_constraint(self.constraint):
                return not DictConstraint.static_validate(self.constraint, value)
            elif Or.is_valid_or_constraint(self.constraint):
                return not self.constraint.validate(value)
            elif Check.is_valid_check_constraint(self.constraint):
                return not Check.static_validate(self.constraint, value)
            return False

    class Multiple:
        """A class that represents multiple constraints in a list-like constraint

        Attributes:
        -----
        constraint
            it can only be a
                1. a type constraint
                2. dictionary constraint
                3. list-like constraint
                4. 'or' constraint
                5. 'check' constraint
        count : int
            Number of constraint it represents.

        Method:
        -----
        is_constraint_valid() -> bool
            Check the validity of the self.constraint
        """

        def __init__(self, constraint, count: int) -> None:
            self.constraint = constraint
            self.count = count

        def __repr__(self) -> str:
            return f"Multiple({self.constraint}, {self.count})"

        def is_constraint_valid(self) -> bool:
            """Check the validity of the self.constraint

            self.constraint can only be:
                1. a type constraint
                2. dictionary constraint
                3. list-like constraint
                4. 'or' constraint
                5. 'check' constraint

            Returns:
                bool: whether self.constraint is valid
            """

            return not not get_constraint_class(self.constraint)

    def __init__(self, constraint: Union[list, tuple]) -> None:
        self.constraint = constraint

    def is_constraint_valid(self) -> bool:
        """Check whether the instance's constraint is a valid list-like constraint

        Returns:
            bool: Whether the instance's constraint is a valid list-like constraint
        """
        return ListLikeConstraint.is_valid_lk_constraint(self.constraint)

    @staticmethod
    def is_valid_lk_constraint(constraint) -> bool:
        """Check whether the constraint is a valid list-like constraint

        A list-like constraint is basically a list or a tuple.
        A list-like constraint's element must be either:
            1. a type constraint
            2. dictionary constraint
            3. list-like constraint
            4. 'or' constraint
            5. 'check' constraint
            6. instance of `Countless` class
            7. instance of `Multiple` class

        Args:
            constraint (any): constraint to be checked

        Returns:
            bool: whether the constraint is a valid list-like constraint
        """

        if type(constraint) not in [list, tuple]:
            return False

        for c in constraint:
            if get_constraint_class(c) or (
                (
                    type(c) == ListLikeConstraint.Countless
                    or type(c) == ListLikeConstraint.Multiple
                )
                and c.is_constraint_valid()
            ):
                continue
            else:
                return False
        return True

    def validate(self, value) -> Union[bool, UnsatisfiedError, InvalidConstraintError]:
        """Validate the value using the instance's list-like constraint.

        Args:
            value (any): value to be validated

        Returns:
            Union[bool, InvalidConstraintError, UnsatisfiedError]: if no complain, return False, else returns error.
        """

        return ListLikeConstraint.static_validate(self.constraint, value)

    @staticmethod
    def static_validate(constraint: Union[list, tuple], value) -> Union[bool, UnsatisfiedError, InvalidConstraintError]:
        """Validate the value using the constraint

        Args:
            constraint (Union[list, tuple]): constraint used
            value (any): value to be validated

        Returns:
            Union[bool, InvalidConstraintError, UnsatisfiedError]: if no complain, return False, else returns error.
        """
        s_constraint = ListLikeConstraint.simplify_constraint(constraint)
        if s_constraint == None:
            return InvalidConstraintError(constraint, ListLikeConstraint)

        if type(value) not in [list, tuple]:
            return UnsatisfiedError(f"Expect the value's type to be either a list or a tuple but the type of value '{value}' is '{type(value).__name__}'")

        offset = 0
        for i, c in enumerate(s_constraint):
            value_i = i + offset

            if value_i >= len(value):
                return UnsatisfiedError(f"The element in the value '{value}' are not enough, stop at constraint index {i}")

            if TypeConstraint.is_valid_type_constraint(c):
                err = TypeConstraint.static_validate(c, value[value_i])
                if err:
                    return err
            elif ListLikeConstraint.is_valid_lk_constraint(c):
                err = ListLikeConstraint.static_validate(c, value[value_i])
                if err:
                    return err
            elif DictConstraint.is_valid_dt_constraint(c):
                err = DictConstraint.static_validate(c, value[value_i])
                if err:
                    return err
            elif Or.is_valid_or_constraint(c):
                err = c.validate(value[value_i])
                if err:
                    return err
            elif Check.is_valid_check_constraint(c):
                err = Check.static_validate(c, value[value_i])
                if err:
                    return err
            elif type(c) == ListLikeConstraint.Countless:
                same_type_count = 0
                while True:
                    # check type
                    if value_i >= len(value) or not c.validate(value[value_i]):
                        if same_type_count < c.at_least:
                            return UnsatisfiedError(f"Not enough element in value '{value}' for {c}, stop at constraint index {i}")
                        else:
                            offset -= 1
                            break
                    else:
                        same_type_count += 1
                        offset += 1
                        value_i = i + offset

        if len(s_constraint) + offset < len(value):
            return UnsatisfiedError(f"Too much element in value '{value}'")
        return True

    @staticmethod
    def simplify_constraint(constraint: Union[list, tuple]) -> Union[None, list, tuple]:
        """Returns simplified version of list-like constraint. Returns None if the constraint given is invalid.

        It does:
            Expands `Multiple` class into types ([Multiple(int, 3)] => [int, int, int])
            Merge `Countless` class with types ([Countless(int, at_least = 1), int, int] => [Countless(int, at_least = 3)])
            Merge `Countless` class with adjecent `Countless class ([Countless(int, at_least=1), Countless(int, at_least=3)] => [Countless(int, at_least = 4)])
        Note: function do not simplify recursively. Nested list-like constraint will not be simplified

        Args:
            constraint (Union[list, tuple]): constraint to be simplified

        Returns:
            Union[None, list, tuple]: simplified version of list-like constraint. None if the constraint given is invalid.
        """

        if not ListLikeConstraint.is_valid_lk_constraint(constraint):
            return None

        constraint_type = type(constraint)

        def expand_mt(constraint: Union[list, tuple]) -> Union[list, tuple]:
            """Expand `Multiple` class in a list-like constraint

            Args:
                constraint (Union[list, tuple]): constraint to be operated

            Returns:
               Union[list, tuple]: expanded version without `Multiple` class
            """
            e = []
            for c in constraint:
                if type(c) == ListLikeConstraint.Multiple:
                    for _ in range(c.count):
                        e.append(c.constraint)
                else:
                    e.append(c)
            return e

        def get_ct_group_info(constraint: Union[list, tuple]) -> list:
            """Group `Countless` class. Assume there is no `Multiple` class.

            Returns list of (group_start, group_end, new_countless)
            Example:
            [int, Countless(int, at_least=1), int, int, str] => [(0, 3, Countless(int, 4))]
            [int, Countless(int, at_least=1), str, int, Countless(int, at_least=2)] => [(0, 1, Countless(int, at_least=2)), (3, 4, Countless(int, at_least=3))]

            Args:
                constraint (Union[list, tuple]): constraint to be operated

            Returns:
                list: list of (group_start, group_end, new_countless)
            """

            result = []
            ct_indexes = [
                i
                for i, c in enumerate(constraint)
                if type(c) == ListLikeConstraint.Countless
            ]
            for ct_i in ct_indexes:
                new_countless = ListLikeConstraint.Countless(
                    constraint[ct_i].constraint, constraint[ct_i].at_least
                )
                group_start = 0
                group_end = len(constraint) - 1
                # find the group_start
                for s_i in range(ct_i - 1, -1, -1):
                    c = constraint[s_i]
                    if (
                        c == new_countless.constraint
                    ):  # found type that is same as Countless' type
                        new_countless.at_least += 1
                    else:  # found other types (no good no good)
                        group_start = s_i + 1
                        break

                # find the group_end
                for s_i in range(ct_i + 1, len(constraint)):
                    c = constraint[s_i]
                    if (
                        type(c) == ListLikeConstraint.Countless
                        and c.constraint == new_countless.constraint
                    ):  # found adjecent countless with same type
                        new_countless.at_least += c.at_least
                        ct_indexes.remove(
                            s_i
                        )  # remove the Countless that will be grouped as it already grouped with this group
                    elif (
                        c == new_countless.constraint
                    ):  # found type that is same as Countless' type
                        new_countless.at_least += 1
                    else:  # found other types (no good no good)
                        group_end = s_i - 1
                        break

                result.append((group_start, group_end, new_countless))
            return result

        expanded = expand_mt(constraint)
        ct_groups = get_ct_group_info(expanded)
        new_constraint = []
        last_end = 0
        for start, end, ct in ct_groups:
            new_constraint = [*new_constraint, *expanded[last_end:start], ct]
            last_end = end + 1
        new_constraint = [*new_constraint, *expanded[last_end:]]
        return constraint_type(new_constraint)


class Or:
    """A class for creating an 'or' constraint

    An 'or' constraint is an instance of `Or` class.
    If the value satisfied any constraint in the constraint list, the value is accepted

    Attributes:
    -----
    constraint : list
        A list or a tuple of constraint, the element can only be:
            1. a type constraint
            2. dictionary constraint
            3. list-like constraint
            4. 'or' constraint (using nested 'or' constraint produce same result but wastes resources, stupid)
            5. 'check' constraint

    Static Method:
    -----
    is_valid_or_constraint(constraint: any) -> Union[bool, UnsatisfiedError, InvalidConstraintError]
        Check whether constraint is a valid 'or' constraint

    Method:
    -----
    validate(value: any) -> bool
        Validate the value using the instance (instance itself is a constraint)
    """

    def __init__(self, *constraint) -> None:
        self.constraint = constraint

    def is_constraint_valid(self) -> bool:
        """Check whether this 'or' constraint is a valid 'or' constraint

        'or' constraint must have a tuple or a list or constraint (self.constraint), where constraint list can only contains:
            1. a type constraint
            2. dictionary constraint
            3. list-like constraint
            4. 'or' constraint (using nested 'or' constraint produce same result but wastes resources, stupid)
            5. 'check' constraint

        Returns:
            bool: whether this 'or' constraint is a valid 'or' constraint

        """

        if type(self.constraint) not in [list, tuple]:
            return False

        for c in self.constraint:
            if get_constraint_class(c):
                continue
            else:
                return False

        return True

    @staticmethod
    def is_valid_or_constraint(constraint) -> bool:
        """Check whether constraint is a valid 'or' cosntraint

        An 'or' constraint is an instance of `Or` class which stores a constraint list.
        The constraint list can be a list or a tuple, which can contain
            1. a type constraint
            2. dictionary constraint
            3. list-like constraint
            4. 'or' constraint (using nested 'or' constraint produce same result but wastes resources, stupid)
            5. 'check' constraint

        Args:
            constraint (any): constraint to be checked

        Returns:
            bool: whether constraint is an valid 'or' constraint
        """

        if type(constraint) != Or:
            return False

        return constraint.is_constraint_valid()

    def validate(self, value) -> Union[bool, UnsatisfiedError, InvalidConstraintError]:
        """Validate the value using the instance (instance itself is a constraint)

        Args:
            value (any): value to be validated

        Returns:
            Union[bool, InvalidConstraintError, UnsatisfiedError]: if no complain, return False, else returns error.
        """

        if not self.is_constraint_valid():
            return InvalidConstraintError("One of the constraint in the constraint list in 'or' constraint is invalid")

        for c in self.constraint:
            if TypeConstraint.is_valid_type_constraint(c):
                if not TypeConstraint.static_validate(c, value):
                    return False
            elif ListLikeConstraint.is_valid_lk_constraint(c):
                if not ListLikeConstraint.static_validate(c, value):
                    return False
            elif DictConstraint.is_valid_dt_constraint(c):
                if not DictConstraint.static_validate(c, value):
                    return False
            elif Or.is_valid_or_constraint(c):
                if not c.validate(value):
                    return False
            elif Check.is_valid_check_constraint(c):
                if not Check.static_validate(c, value):
                    return False
        return UnsatisfiedError(f"The value '{value}' does not satisfied any of the constraints")


class Check:
    """A class that checks value through check constraint

    The check constraint is a function that accepts only one value as an argument.
    The value to be validated will be passed into check constraint as an argument.
    If check constraint returns False, there is no complain, value satisfies the constraint.
    If check constraint returns an error, there is a complain.
    It is like a user-defined constraint.

    Attributes:
    -----
    constraint : FunctionType
        The check constraint

    Static Method:
    -----
    is_valid_check_constraint(constraint: any) -> bool
        Check whether the constraint is a valid check constraint
    static_validate(constraint: FunctionType, value: any) -> bool
        Validate the value using the constraint

    Method:
    -----
    is_constraint_valid() -> bool
        Check whether the instance's constraint is a check constraint
    validate(value: any) -> Union[bool, UnsatisfiedError, InvalidConstraintError]
        Validate the value using the check constraint (returns the result of check constraint function call)

    """

    def __init__(self, constraint: FunctionType) -> None:
        self.constraint = constraint

    def is_constraint_valid(self) -> bool:
        """Check whether the instance's constraint is a check constraint

        Returns:
            bool: whether the instance's constraint is a check constraint
        """

        return Check.is_valid_check_constraint(self.constraint)

    @staticmethod
    def is_valid_check_constraint(constraint) -> bool:
        """Check whether the constraint is a valid check constraint

        Args:
            constraint (any): constraint to be checked

        Returns:
            bool: whether the constraint is a valid check constraint
        """

        return type(constraint) == FunctionType and constraint.__code__.co_argcount == 1

    def validate(self, value) -> Union[bool, UnsatisfiedError, InvalidConstraintError]:
        """Validate the value using the instance's check constraint

        It validates by returning the result of the instance's check constraint function call.
        It returns False if the constraint is invalid.

        Args:
            value (any): value to be validated

        Returns:
            Union[bool, InvalidConstraintError, UnsatisfiedError]: if no complain, return False, else returns error.
        """
        return Check.static_validate(self.constraint, value)

    @staticmethod
    def static_validate(constraint: FunctionType, value) -> Union[bool, UnsatisfiedError, InvalidConstraintError]:
        """Validate the value using the check constraint

        It validates by returning the result of the check constraint function call.
        It returns False if the constraint is invalid.

        Args:
            constraint (FunctionType): A check constraint
            value: value to be validated

        Returns:
            Union[bool, InvalidConstraintError, UnsatisfiedError]: if no complain, return False, else returns error.
        """
        if not Check.is_valid_check_constraint(constraint):
            return InvalidConstraintError("The check constraint is invalid")

        err = constraint(value)
        return err and UnsatisfiedError(err)


def get_constraint_class(
    constraint,
) -> Union[TypeConstraint, DictConstraint, ListLikeConstraint, Or, Check, None]:
    """Get the class that handles the constraint

    Args:
        constraint (any): constraint to be validated

    Returns:
        Union[TypeConstraint, DictConstraint, ListLikeConstraint, Or, Check, None]: class that handles the constraint

    """
    if TypeConstraint.is_valid_type_constraint(constraint):
        return TypeConstraint
    elif DictConstraint.is_valid_dt_constraint(constraint):
        return DictConstraint
    elif ListLikeConstraint.is_valid_lk_constraint(constraint):
        return ListLikeConstraint
    elif Or.is_valid_or_constraint(constraint):
        return Or
    elif Check.is_valid_check_constraint(constraint):
        return Check
    else:
        return None
