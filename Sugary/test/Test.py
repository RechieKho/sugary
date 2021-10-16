"""
Test class that writes test easily
"""

from ..shared import log

class Test:
    class Compare:
        def __init__(self, test_obj, test_description, a) -> None:
            self.test_description = test_description
            self.test_obj = test_obj
            self.a = a

        def equal_to(self, b):
            """
            Expecting self.a == b.
            """
            self.test_obj._Test__check_test_result(self.test_description, self.a == b) # accessing the private method of Test
        
        def to_be(self, b):
            """
            Expect self.a and b is the same thing 
            """
            self.test_obj._Test__check_test_result(self.test_description, self.a is b) # accessing the private method of Test
        
        def not_equal_to(self, b):
            """
            Expecting self.a != b
            """
            self.test_obj._Test__check_test_result(self.test_description, self.a != b) # accessing the private method of Test
        
        def not_to_be(self, b):
            """
            Expecting self.a and b is not the same
            """
            self.test_obj._Test__check_test_result(self.test_description, self.a is not b) # accessing the private method of Test
        
    class Expect:
        def __init__(self, test_obj,  test_description) -> None:
            self.test_description = test_description
            self.test_obj = test_obj

        def expect(self, a):
            return Test.Compare(self.test_obj, self.test_description, a)
    
    def __init__(self, title: str, strict = True) -> None:
        self.title = title
        self.strict = strict
        print()
        print(log.make_heading(f"Start Test: `{title}` | strict = {strict}"))

    def about(self, test_description:str):
        return Test.Expect(self, test_description)
    
    def __check_test_result(self, test_description: str, is_success: bool):
        if is_success:
            Test.__print_test_success(test_description)
        else:
            Test.__print_test_fail(test_description)
            if self.strict:
                print(log.s("This is a strict test. Exit.", "red"))
                exit(0)
    
    @staticmethod
    def __print_test_success(test_description: str) -> None:
        print(f"[ {log.s('S', fg_color='green')} ] {log.s(test_description, styles='bold')}")
    
    @staticmethod
    def __print_test_fail(test_description: str) -> None:
        print(f"[ {log.s('F', fg_color='red')} ] {log.s(test_description, styles='bold')}")

if __name__ == "__main__":
    sanity_check = Test("Sanity Check", strict = False)
    sanity_check.about("is `a` and `b` not the same").expect("a").not_to_be("b")
    sanity_check.about("sky same as blue").expect("Sky").to_be("blue")

    test_a = Test("Test a")
    test_a.about("is 1 equal to 1").expect(1).equal_to(1)
    test_a.about("Must be wrong").expect(2).to_be(3)


