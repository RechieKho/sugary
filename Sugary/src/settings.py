"""
Provides CONSTANTS for other python scripts
"""

class USERFILE: # information about user's file (for configuring Sugary)
    SGR_DIR_NAME = ".sgr" # directory name for storing Sugary's configuration files
    class SETTING: # SETTING module
        MOD_NAME = "settings" # module name
        CONFIG_FUNC_NAME = "configure" # name of function that will be run to get the configuration
        CONTROL_FUNC_NAME = "control" # name of function that will be run to allow user control the life cycle of Sugary
