# pepp9i
Translates pep91 and pep92 programs into pep9

My goal with this project is to make it easier to develop larger pep92 projects by improving the way external libraries are loaded.  As of right now I am still working on writing a functional pep9i compiler so right now the compiler just looks for additional files inside the project folder.

```.pep1``` and ```.pep2``` files can be compiled using this command assuming you have all the included or appended files inside the project directory.
```
python pep91c.py filename.pep2
```
This project is at a very early stage so it does not have good compatibility and only works with simple pep9i programs

**To Do**

- [x] Implement ```.INCLUDE```
- [x] Implement ```.APPEND```
- [x] Implement collision resolution
- [x] Implement ```.GLOBAL```
- [x] Implement ```.MACRO``` and ```.MACROEND```
- [ ] Improve compiler comments
- [ ] Remove random empty lines in output code
- [ ] Fix formatting on output code
- [ ] Add external library support
- [ ] Improve code quality

**Syntax**

|Symbol|Example|Description|
| --- | --- | --- |
|```.INCLUDE```|```.INCLUDE    "macros.pep2"```|Inserts file right there|
|```.APPEND```|```.APPEND    "heap.pep2"```|Appends file to end|
|```.GLOBAL```|```.GLOBAL    strLen```|Defines variable as global|
|```.MACRO```|```.MACRO    DECO    5,stx```|Begins macro
|```.MACROEND```|```.MACROEND```|Ends macro