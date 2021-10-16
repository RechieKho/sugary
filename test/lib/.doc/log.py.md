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
The aim of this documentation is to explain the purpose of functions and classes of this python script (`test/lib/log.py`). 
<br>
<br>
# Classes 
<div class="classes">Colors()</div>
---

## Description
It is a class that only stores data for creating ansi escape codes to set the color and the style of the text.

## Static variables

| identifier | description |
| ----- | ----- |
| `prefix` | A `str`. It is a prefix for creating ansi escape code for creating color text. (`f"{prefix}{code}{suffix}"`) |
| `suffix` | A `str`. It is a suffix for ending the ansi escape code, pair with `prefix` to create a ansi escape code. (`f"{prefix}{code}{suffix}"`) |
| `fg_color` | A `dict`. Paired with `prefix` and `suffix` to create an ansi escape code that set the foreground color of the text after the escape code. (`f"{prefix}{fg_color['color_name']}{suffix}"`) |
| `bg_color` | A `dict`. Paired with `prefix` and `suffix` to create an ansi escape code that set the background color of the text after the escape code. (`f"{prefix}{bg_color['color_name']}{suffix}"`) |
| `styles` | A `dict`. Paired with `prefix` and `suffix` to create an ansi escape code that set the styles (bold, underline and etc.) of the text after the escape code. (`f"{prefix}{styles['color_name']}{suffix}"`) |
| `reset` | A `str`. The ansi escape code that clear all the color and style changes |

<br>
<br>

# Functions 
<div class="functions">s(text: str, fg_color = '', bg_color = '', styles = '')</div>
--- 

## Description
The `s` stands for `style`. It is a helper function that returns styled text using the `Colors` class based on arguments. 

## Parameters

| identifier | description |
| ----- | ----- | 
| `text` | A `str`. Texts to be styled |
| `fg_color` | A `str`. Empty string by default. Color of the styled text. Will not style the text if it is not in `Colors.fg_color`. |
| `bg_color` | A `str`. Empty string by default. Background color of the styled text. Will not style the text if it is not in `Colors.bg_color`. |
| `styles` | A `str`. Empty string by default. Style (bold, underline and etc.) of the styled text. Will not style the text if it is not in `Colors.styles`. |

## Return value
Returns styled text based on arguments given. 

<br>
---
<div class="functions">cut_text(text: str, column_count, max_constrict = 20, max_expand = 20)</div>
---

## Description
It cuts the text into a list of rows of text segment. It only cut at space. it is used to control the width of the text that will be printed to the console. 

if we pass
`"This is a a long text.\n This is a really long text. This is a really really long text"`,
into the `cut_text` function, it returns: 
```
[
    'This is a long text. ',
    '',
    'This is a really ',
    'long text.',
    'This is a ',
    'really really long',
    'text'
]
```

| Note: Ansi escape are also charaters as well...

## Parameters

| identifier | description |
| ----- | ----- |
| `text` | A `str`. Text to be cut. |
| `column_count` | An `int`. How many character in one segment of text. |
| `max_constrict` | An `int`. Max constriction of character in one segment of text. |
| `max_expand` | An `int`. Max expansion of character in one segment of text. |

## Return value
Return a list of segment of text.

<br>
---
<div class="functions">make_billboard(title: str, text: str, width: int, title_style = {"styles": "bold"})</div>
---

## Description
it makes and returns a string of text that looks like a 'billboard' when printed.

when we run 
`print(make_billboard(" Dear madam, ", f"I don't think you know why this texts are so colorful, good luck on finding out ", 75))`,
it will print out
```
 ╭-- Dear madam, ---------------------------------------------------------------+
 |  I don't think you know why this texts are so colorful,
 |  good luck on finding out
 ╰------------------------------------------------------------------------------+
```

## Parameters

| identifier | description |
| ----- | ----- | 
| `title` | A `str`. Title of the billboard. |
| `text` | A `str`. Content of the billboard. |
| `width` | An `int`. The with of billboard in characters. |
| `title_style` | A `dict`. The style of the title. Note that this is the only way to style the title, passing styled text into `title` may cause unwanted behaviour. |

## Return Value
Return a string of text that resemble a billboard when printed.

<br>
---
<div class="functions">make_horizontal_line()</div>
---

## Description
It returns a string of 58 dashes.

## Parameters
No parameters

## Return Value
Return a string of 58 dashes.

<br>
---
<div class="functions">make_heading(text: str)</div>
---

## Description
It returns an underlined text (A heading ok?).

## Parameters
| identifier | description |
| ----- | ----- |
| `text` | A `str`. The text of heading |

## Return Value
A heading string (an underlined text)

<br>
---
<div class="functions">make_warning(text: str)</div>
---

## Description
A specialized `make_billboard`. Title of billboard always `WARNING`.

## Parameters
| identifier | description |
| ----- | ----- | 
| `text` | A `str`. Content of the warning billboard. |

## Return Value
A warning billboard.

<br>
---
<div class="functions">make_warning(text: str)</div>
---

## Description
A specialized `make_billboard`. Title of billboard always `ERROR`.

## Parameters
| identifier | description |
| ----- | ----- | 
| `text` | A `str`. Content of the error billboard. |

## Return Value
An error billboard.


## [return to directory](./main.md)