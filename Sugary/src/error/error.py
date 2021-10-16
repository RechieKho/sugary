"""
Provides function for error handling
"""

from ...shared import log

def err(err_desc:str):
    print(log.make_error(err_desc))
    exit(0)

