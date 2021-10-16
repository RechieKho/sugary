<style>
.classes { /* for classes*/
    color: #F1FAEE;
    font-weight: bold;
    background: #1D3557;
    border-radius: 1rem;
    padding: 1rem;
    text-align: center;
}

.functions{
    color: #F1FAEE;
    font-weight: 500;
    background: #E63946;
    border-radius: 1rem;
    padding: 1rem;
    text-align: center;
}
</style>
# DOCUMENTATION ⚙⚙⚙
The aim of this documentation is to explain the purpose of functions and classes of this python script (`/test/lib/Test.py`). 
<br>
<br>

# Dependency
This python script do not depends on: 
- `/shared/log.py`
  
<br>
<br>

# Classes

<div class="classes">Test(title: str, strict = True)</div>
--- 

## Description
A class that makes writing test easily and comprehensible. Unfortunately, in order to make the written test intuitive, some classes are created just for the sake of it. This causes the interanl working of `Test` class miserably hard to explain. Luckily, the test are easy to write and no extra configuration need to be considered (guarantee no information blindness). Thus, I will only explain how to use it.

## How to use:
```python
sanity_check = Test("Sanity Check", strict = False)
sanity_check.about("is `a` and `b` not the same").expect("a").not_to_be("b")
sanity_check.about("sky same as blue").expect("Sky").to_be("blue")
sanity_check.about("is 1 equal to 1").expect(1).equal_to(1)
sanity_check.about("is 1 not equal to 2").expect(1).not_equal_to(2)
```

Above are the **only** ways to use the `Test` class...
1. First, start a test by initialize `Test` class by passing in the title of the test. `strict` parameter is `True` by default, this causes the test to be quited when there is a failed test. Setting `strict` to `False` means ignore failed test.
2. Then, the `about` method is used to give a name to the test you are about to make. Please write a sensible one.
3. `expect` method is chained with `about`. This is the only "chaining" method you can used after `about`.
4. After `expect`, you can chain it with `to_be`, `not_to_be`, `equal_to`, and `not_equal_to`, which are all self-explanatory when chained together. All of the chained method takes only 1 argument.
5. Run the test script. It will print out the result into the console.

## [Return to Directory](main.md)