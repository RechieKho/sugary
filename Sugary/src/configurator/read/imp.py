"""
Provide function to import setting (.sgr/Setting.py file) from user
It only try get the configure and control function in user's setting (defined in USERFILE class in `Sugary/src/settings.py`)

configure function is compulsary while control function is optional
The name of the functions can be changed in `Sugary/src/settings.py`
"""

import importlib.util as u
from types import FunctionType

from ...settings import USERFILE
from ...error.core import err

def import_setting():
    """
    Import user's settings and returns list of functions (configure function and control function).
    Note that configure function is compulsary while control function is optional.
    So the length of the list varies between one and two
    """
    setting_path = f"{USERFILE.SGR_DIR_NAME}/{USERFILE.SETTING.MOD_NAME}.py"

    # import setting module
    try:
        module = u.spec_from_file_location(USERFILE.SETTING.MOD_NAME, setting_path).loader.load_module(USERFILE.SETTING.MOD_NAME)
    except FileNotFoundError:
        err(f"Unable to find {setting_path} ☹ , please create one and try again...")
    
    # find the configure and control function
    funcs = []
    # get configure function
    if hasattr(module, USERFILE.SETTING.CONFIG_FUNC_NAME) and type(getattr(module, USERFILE.SETTING.CONFIG_FUNC_NAME)) == FunctionType:
        funcs.append(getattr(module, USERFILE.SETTING.CONFIG_FUNC_NAME))
    else:
        err(f"Unable to find `{USERFILE.SETTING.CONFIG_FUNC_NAME}` function in {setting_path}. It is required to configure the system.")
    # get control function
    (hasattr(module, USERFILE.SETTING.CONTROL_FUNC_NAME) and type(getattr(module, USERFILE.SETTING.CONTROL_FUNC_NAME)) == FunctionType) and funcs.append(getattr(module, USERFILE.SETTING.CONTROL_FUNC_NAME))
    return funcs
    



if __name__ == "__main__":
    import_setting()
