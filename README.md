# pepp9i
Translates pep9i programs into pep9

This project is still in beta and will not have perfect compatibility with all pep9i programs. **Use this software at your own risk.**

## Table of Contents
 - [Goal](#goal)
 - [Vocabulary](#vocabulary)
 - [Usage](#usage)
 - [Todo](#todo)
 - [Syntax Reference](#syntax)

# Goal
My goal with this project is to create an open source pep9i compiler written in python to make changes and enhancements easier. I would also like to add an improved file importing system to prevent cluttering the project folder and accidentally committing library files to github.


# Vocabulary
Throughout this documentation you may see pep9i files be referred to as ```pep92```, ```pep91``` or simply ```pepi```. They all essentially mean the same thing and the compiler itself makes no distinction between the file types. You could call your pep9i programs whatever you want as the extension is required in the filename. In the future I would like to shift to using ```.pepi``` as the default pep9i file extension but for now this compiler does not check.


# Usage

```.pep1``` and ```.pep2``` files can be compiled using this command assuming you have all the included or appended files inside the project directory.
```
python pep91c.py filename.pep2
```


# Todo

- [x] Implement all pep9 instructions
- [x] Improve error handling and detection (print line number and file of incorrect syntax)
- [ ] Load imports from another location
- [ ] Organize external imports in folders
- [ ] Create auto updater and installer
- [x] Add compiler options like removing comments or printing imported files

# Syntax

These are the default methods included within the pepi compiler. Typically pep9i or pep92 are bundled with a macros file to enhance the existing pep architecture but they are not included here.

|Symbol|Example|Description|
| --- | --- | --- |
|```.INCLUDE```|```.INCLUDE    "macros.pep2"```|Inserts file right there|
|```.APPEND```|```.APPEND    "heap.pep2"```|Appends file to end|
|```.GLOBAL```|```.GLOBAL    strLen```|Defines variable as global|
|```.MACRO```|```.MACRO    DECO    5,stx```|Begins macro
|```.MACROEND```|```.MACROEND```|Ends macro