"""
Provide function to test Sugary.src.configurator
"""

from ..src.configurator.read import imp

from .core import Test

def test_imp(): # test imp.py
    test = Test("imp.py")
    
    # Note: Any changes in /.sgr/settings.py requires code below to be rewritten
    settings = imp.import_setting()
    test.about("`import_setting` function returns a list with the length of 1").expect(len(settings)).to_be(1) # this follows the /.sgr/settings.py
    config = settings[0]()
    test.about("configuration function returns dictionary same as return value of`configure` function in /.sgr/settings.py").expect(config).equal_to([
        {
            "test": 1
        }
    ])

    
    
