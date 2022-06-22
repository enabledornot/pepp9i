import pep9lib
def resolveCollisions(code):
    global globalVars
    global usedVars
    global colCount
    globalVars = []
    usedVars = []
    colCount = 0
    newCMD = []
    for i in code:
        for ii in i.split("\n"):
            newCMD.append(command(ii))
            split = pep9lib.splitArgs(ii)
            if split[0]==".GLOBAL":
                globalVars.append(split[1])
class command:
    def __init__(self,stri):
        self.pointer = pep9lib.getRef(stri)
        self.inst = pep9lib.getInst(stri)
        self.args = pep9lib.getArgs(stri)
        self.com = pep9lib.getComments(stri)
    def __str__(self):
        return self.rebuild()
    def isPoint(self):
        if self.pointer=="":
            return False
        return True
    def rebuild(self):
        newStr = ""
        if self.pointer!="":
            newStr+=self.pointer + ": "
        if self.inst!="":
            newStr+=self.inst + " "
        if len(self.args)!=0:
            newStr+=",".join(self.args) + " "
        if self.com!="":
            newStr+=self.com
        return newStr
