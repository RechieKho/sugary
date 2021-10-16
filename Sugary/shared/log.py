"""
Logger functions to log stuff efficiently
"""

# --- backend --- 

class Colors: 
    """
    It is a class that only stores data for creating ansi escape codes to set the color and the style of the text.
    """
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

# style text
def s(text : str, fg_color = '', bg_color = '', styles = '') -> str:
    """
    The `s` stands for `style`. It is a helper function that returns styled text using the `Colors` class based on arguments. 
    """

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
           f'{Colors.reset}'

def cut_text(text:str, column_count: int, max_constrict = 20, max_expand = 20) -> list[str]:
    """
    It cuts the text into a list of rows of text segment. It only cut at space. it is used to control the width of the text that will be printed to the console. 
    """
    dirty_chunks = []
    cut_point = list(range(0, len(text), column_count))
    for i in range(len(cut_point)):
        if i + 1 >= len(cut_point):
            dirty_chunks.append(text[cut_point[i]:])
        else:
            constriction = 0
            expansion = 0
            right_char_index = cut_point[i+1] 
            left_char_index = cut_point[i+1] - 1
            is_cuttable = text[right_char_index] == ' ' or text[left_char_index] == ' '
            if not is_cuttable:
                while right_char_index + 1 < len(text) and left_char_index - 1 >= 0:
                    # march until we met a space
                    if expansion < max_expand:
                        right_char_index += 1
                        expansion += 1
                        if text[right_char_index] == ' ':
                            # update cut_point and cut
                            cut_point[i + 1] = right_char_index + 1
                            break
                    if constriction < max_constrict:
                        left_char_index -= 1
                        constriction += 1
                        if text[left_char_index] == ' ':
                            #update cut_point and cut
                            cut_point[i + 1] = left_char_index + 1
                            break
                    if constriction >= max_constrict and expansion >= max_expand:
                        break
            elif text[right_char_index] == ' ':
                cut_point[i + 1] = right_char_index + 1
            dirty_chunks.append(text[cut_point[i]: cut_point[i+1]])
    
    chunks = []
    for i in [ i.split("\n") for i in dirty_chunks if i != '']: # clean dirty chunks
        for splitted_segment in i:
            chunks.append(splitted_segment)
    return chunks
    
# -- frontend ---

def make_billboard(title:str, text:str, width:int, title_style = {"styles" : "bold"}) -> str:
    """
    it makes and returns a string of text that looks like a 'billboard' when printed.
    """
    display_width = width + 8
    rows_of_text = cut_text(text, display_width - 8, max_expand=0, max_constrict=display_width)

    # generate text
    content = ""
    for row in rows_of_text:
        content += " |  " + row + "\n"
    section = f' ╭--{s(title, **title_style)}' + '-'*(display_width - 8 - len(title)) + '-+  \n' \
            f'{content}' \
                f' ╰--' + "-"*(display_width - 8) + '-+  '
    return section

def make_horizontal_line() -> str:
    """
    It returns a string of 58 dashes.
    """
    return "-"*58

def make_heading(text:str) -> str:
    """
    It returns an underlined text (A heading ok?).
    """
    return s(text, styles = 'underline') 

def make_error(text:str) -> str:
    """
    A specialized `make_billboard`. Title of billboard always `ERROR`.
    """
    return make_billboard(" ERROR ", text, 50, {"fg_color": "red"})

if __name__ == "__main__":
    # Test log.py
    print(make_heading("Test `log.py`"))
    print("Test `s` function...\n")
    print(s("This is stylized text with red foreground, green background, and bold font", "red", "green", "bold"))
    print(s("This is stylized text with black foreground, white background, and blink font", "black", "white", "blink"))
    print(s("This is stylized text without any flavour"))
    print(s("This is bold text", '', '', 'bold'))

    print(make_horizontal_line())
    print("Test `cut_text` function...\n")
    text = "This is a a long text. This is a really long text. This is a really really long text"
    print(f"text to be cut: '{text}'")
    print(cut_text(text, 20))

    print(make_horizontal_line())
    print("Test `make_billboard` function...\n")
    print(make_billboard(" test ", "This is a really good section", 25))
    print(make_error("GOD IS DEAD"))
    print(make_billboard(" Dear madam, ", f"I don't think you know why this texts are so {s('colorful', fg_color='green', bg_color='light_blue')}, good luck on finding out {s('LOL', fg_color='red')}", 75))

