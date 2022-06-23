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
            print(newCMD[-1])
            if newCMD[-1].inst==".GLOBAL":
                globalVars.append(newCMD[-1].args[0])
                newCMD[-1] = command(";"+ii)
    print(globalVars)
    resolveCollisionsRec(newCMD,0)
    for i in range(len(code)):
        code[i] = newCMD[i].__str__()
def resolveCollisionsRec(code,lineNumb):
    count = lineNumb
    localVars = {}
    while len(code)>count and not code[count].getBeginCom()=="}":
        if code[count].getBeginCom()=="{":
            count = resolveCollisionsRec(code,count+1)
        else:
            resolveLine(code[count],localVars)
        count+=1
    return count
def resolveLine(command,localVars):
    global usedVars
    global globalVars
    global colCount
    if command.pointer!="":
        if (command.pointer not in globalVars):
            if(command.pointer in usedVars):
                localVars[command.pointer] = "ZZ"+str(colCount)
                command.pointer = localVars[command.pointer]
                colCount+=1
            else:
                usedVars.append(command.pointer)
    for i in range(len(command.args)):
        if command.args[i] in localVars:
            command.args[i] = localVars[command.args[i]]
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
