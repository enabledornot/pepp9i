![pepplus logo](peppluslogo.png)
# PEPplus
Translates PEPplus and pep9i programs into pep9

This project is still in beta and will not have perfect compatibility with all pep9i programs. **Use this software at your own risk.**

## Table of Contents
 - [Goal](#goal)
 - [Vocabulary](#vocabulary)
 - [Usage](#usage)
 - [Todo](#todo)
 - [Syntax Reference](#syntax)

# Goal
The goal of this project is to create an open source pepplus/pep9i compiler written in python to make changes and enhancements easier. I would also like to add an improved file importing system to prevent cluttering the project folder and accidentally committing library files to github.


# Vocabulary
PEPplus refers to this project and the architecture created by this project. Pep9i refers to the existing pep9i architecture and compiler included in the original project. Files designed for the original pep9i compiler usually have the extention ```.pep2``` or ```.pep1```.

# Usage

```.pep1```,```.pep2``` and ```.pepp``` files can be compiled using this command assuming you have all the included or appended files inside the project directory.
```
python pep91c.py filename.pepp
```


# Todo

- [x] Implement all pep9 instructions
- [x] Improve error handling and detection (print line number and file of incorrect syntax)
- [ ] Load imports from another location
- [ ] Organize external imports in folders
- [ ] Create auto updater and installer
- [x] Add compiler options like removing comments or printing imported files

# Syntax

These are the default methods included within the PEPplus compiler. Typically pep9i or pep92 are bundled with a macros file to enhance the existing pep architecture but they are not included here.

This compiler loads external files differently depending on the extension provided. If you import a ```.pep2``` or ```.pep1``` file it will assume you are using legacy imports and search all included sub directories for files matching that name. If you import any other filetype it assumes you are using the new import mode and it assumes you are loading the library directly. This new import mode uses ```.``` in place of ```/```. If you wanted to load the file called ```peplib/main.pepp``` from your program folder you would use ```.INCLUDE    peplib.main.pepp```.


|Symbol|Example|Description|
| --- | --- | --- |
|```.INCLUDE```|```.INCLUDE    "macros.pep2"```|Inserts file right there|
|```.APPEND```|```.APPEND    "heap.pep2"```|Appends file to end|
|```.GLOBAL```|```.GLOBAL    strLen```|Defines variable as global|
|```.MACRO```|```.MACRO    DECO    5,stx```|Begins macro
|```.MACROEND```|```.MACROEND```|Ends macro