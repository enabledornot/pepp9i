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
    resolveCollisionsRec(newCMD,0)
def resolveCollisionsRec(code,lineNumb):
    count = lineNumb
    while len(code)>count and not code[count].getBeginCom()=="}":
        if code[count].getBeginCom()=="{":
            count = resolveCollisionsRec(code,count+1)
        else:
            None
            # print(code[count])
        count+=1
    return count
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
    def hasArgs(self):
        if len(self.args)==0:
            return False
        return True
    def getBeginCom(self):
        if len(self.com)<2:
            return ""
        return self.com[1]
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
