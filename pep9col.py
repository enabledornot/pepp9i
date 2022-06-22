import pep9lib
def resolveCollisions(code):
    global globalVars
    global usedVars
    global colCount
    globalVars = []
    usedVars = []
    colCount = 0
    for i in code:
        split = pep9lib.splitArgs(i)
        if split[0]==".GLOBAL":
            globalVars.append(split[1])
class command:
    def __init__(self,stri):
        self.pointer = pep9lib.getRef(stri)
        self.inst = pep9lib.getInst(stri)
        self.args = pep9lib.getArgs(stri)
        self.com = pep9lib.getComments(stri)
    def rebuild(self):
        newStr = ""
        if self.pointer!="":
            newStr+=self.pointer + " "
        if self.inst!="":
            newStr+=self.inst + " "
        if self.args!="":
            newSt+=",".join(self.args)
