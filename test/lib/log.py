"""
Logger functions to log stuff efficiently
"""

import os
from math import ceil

# --- backend --- 

class Colors: 
    prefix = '\033[1;'
    suffix = 'm'
    fg_color = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'default': 39,
        'light_gray': 37,
        'dark_gray': 90,
        'light_red': 91,
        'light_green': 92,
        'light_yellow': 93,
        'light_blue': 94,
        'light_magenta': 95,
        'light_cyan': 96,
        'white': 97
    }
    bg_color = {
        'black': 40,
        'red': 41,
        'green': 42,
        'yellow': 44,
        'blue': 44,
        'magenta': 45,
        'cyan': 46,
        'default': 49,
        'light_gray': 47,
        'dark_gray': 100,
        'light_red': 101,
        'light_green': 102,
        'light_yellow': 103,
        'light_blue': 104,
        'light_magenta': 105,
        'light_cyan': 106,
        'white': 107,
    }
    styles = {
        'bold': 1,
        'dim': 2,
        'underline': 4,
        'blink': 5,
        'reverse': 7,
        'hidden': 8,
    }
    reset = f'{prefix}0{suffix}'

# stylize text
def s(text, fg_color = '', bg_color = '', styles = ''):

    is_in_dict = lambda key, dictionary: key in dictionary or ''

    genSeq = lambda style_type : {
        "fg" : lambda x : is_in_dict(x, Colors.fg_color) and f'{Colors.prefix}{Colors.fg_color[x]}{Colors.suffix}',
        "bg" : lambda x : is_in_dict(x, Colors.bg_color) and f'{Colors.prefix}{Colors.bg_color[x]}{Colors.suffix}',
        "styles" : lambda x : is_in_dict(x, Colors.styles) and f'{Colors.prefix}{Colors.styles[x]}{Colors.suffix}',
    }[style_type]

    return f'{genSeq("fg")(fg_color)}'\
           f'{genSeq("bg")(bg_color)}'\
           f'{genSeq("styles")(styles)}'\
           f'{text}'\
           f'{is_in_dict(fg_color, Colors.fg_color) and Colors.reset}'\
           f'{is_in_dict(bg_color, Colors.bg_color) and Colors.reset}'\
           f'{is_in_dict(styles, Colors.styles) and Colors.reset}'

def get_console_dimenstion():
    return os.popen('stty size', 'r').read().split()

# -- frontend ---

def make_horizontal_line():
    return "----------------------------------------------------"

def make_heading(text):
    return s(text.title(), styles = 'underline') + "\n"

def make_warning():
    pass

if __name__ == "__main__":
    # Test log.py
    print(make_heading("Test `log.py`"))
    print("Test `stylize` function...\n")
    print(s("This is stylized text with red foreground, green background, and bold font", "red", "green", "bold"))
    print(s("This is stylized text with black foreground, white background, and blink font", "black", "white", "blink"))
    print(s("This is stylized text without any flavour"))
    print(s("This is bold text", '', '', 'bold'))

