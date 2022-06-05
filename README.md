# pepp9i
Translates pep91 and pep92 programs into pep9

My goal with this project is to make it easier to develop larger pep92 projects by improving the way external libraries are loaded.

`.pep1' and '.pep2' files can be compiled using this command assuming you have all the included or appended files.
```
python pep91c.py filename.pep2
```
This project is at a very early stage so it might not have perfect compatibility.

**To Do**

- [x] Implement ```.INCLUDE```
- [x] Implement ```.APPEND```
- [x] Implement collision resolution
- [ ] Implement ```.GLOBAL```
- [x] Implement ```.MACRO``` and ```.MACROEND```
- [ ] Improve compiler comments