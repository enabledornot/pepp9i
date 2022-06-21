import pep9term
import sys
def cleanUp(string):
    block = string.split("\n")
    nblock = []
    for i in block:
        if len(i)!=0 and i[0]!=" ":
            nblock.append(i)
    return nblock
def compare(string0,string1):
    clean0 = cleanUp(string0)
    clean1 = cleanUp(string1)
    for i in range(len(clean0)):
        if clean0[i]!=clean1[i]:
            print(i)
            print(clean0[i])
            print(clean1[i])
            print("----------")
input0 = pep9term.compilel(sys.argv[1])
input1 = pep9term.compilel(sys.argv[2])
compare(input0,input1)