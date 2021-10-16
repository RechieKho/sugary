# DOCUMENTATION ⚙⚙⚙
The aim of this documentation is to explain the purpose of directory, modules, functions and classes of this codebase. 

## Directory Structure 

```
./
| - shared/
| - src/
| - test/
    | - lib/
```

### Description of each directory
1. [`shared/`](shared/.doc/main.md) - contains source code that accessible to all directory (by using link)
2. [`src/`](src/.doc/main.md) - contains source code for this project
3. [`test/`](test/.doc/main.md) - contains files to test the functionality of the source code
   1. [`lib/`](test/lib/.doc/main.md) - contains python scripts which provides functions and classes to write tests. 

## Files
These are the rough description of the files in current directory.

| filename | description |
| ----- | ----- |
| `README.md` | a normal markdown file that contains description of this project |
| `test.py` | entry point of test file. Run it to test the source code. |