"""
Entry point of the test file. Run this python script to test the functionality of source code. 
"""

from Sugary.test import (
    test_configurator as ts_c,
)


def test():
    """
    entry point of the test file
    """
    ts_c.test_imp() # test Sugary/src/configurator/read/imp.py
    pass

if __name__ == "__main__":
    test()
