# General library for dealing with pep9 assembly in python


def splitArgs(stri):
    args = [""]
    inQuotes = False
    for i in stri:
        if i=="\"":
            inQuotes = not(inQuotes)
        if i==" " and not(inQuotes):
            if args[-1]!="":
                args.append("")
        else:
            args[-1]+=i
    return args
def getRef(cmd):
    cmd = removeComments(cmd)
    split = splitArgs(cmd)
    if len(split)==0 or len(split[0])==0:
        return ""
    if split[0][-1]==":":
        return split[0][:-1]
    return ""
def getInst(cmd):
    cmd = removeComments(cmd)
    split = splitArgs(cmd)
    if len(split)==0 or len(split[0])==0:
        return ""
    if split[0][-1]==":":
        split.pop(0)
    return split[0]
def getArgs(cmd):
    cmd = removeComments(cmd)
    split = splitArgs(cmd)
    if len(split)==0 or len(split[0])==0:
        return []
    if split[0][-1]==":":
        split.pop(0)
    if len(split)<=1:
        return []
    args = []
    for i in split[1:]:
        splits = i.split(",")
        if "" in splits:
            splits.remove("")
        args.append(splits)
    return args
def findQuotedData(strt):
    pos = 0
    indata = ""
    prevBak = False
    inQuotes = False
    for i in strt:
        if prevBak:
            if inQuotes:
                indata+=i
        else:
            if i=="\"":
                inQuotes = not(inQuotes)
            else:
                if inQuotes:
                    indata+=i
        pos+=1
    return indata
def formatFix(codeList,space=[10,10,10]):
    count = 0
    while len(codeList)>count:
        codeList[count] = formatLine(codeList[count],space=space)
        count+=1
def formatLine(codeLine,space=[10,10,10]):
    if isinstance(codeLine,command):
        return codeLine.formatLine(space=space)
    if len(codeLine)==0 or codeLine[0]==";":
        return codeLine
    lineSplit = codeLine.split(";",1)
    codeLine = lineSplit[0]
    if len(lineSplit)==1:
        comLine = ""
    else:
        comLine = ";"+lineSplit[1]
    split = splitArgs(codeLine)
    if len(split)<2:
        return codeLine
    newLine = ""
    count = 0
    for i in split[:-1]:
        newLine+=pad(i,space[count])
        if count!=len(space)-1:
            count+=1
    newLine+=split[-1]
    return newLine + comLine
def pad(stri,leng,chart=' '):
    return stri + (leng-len(stri))*chart
def removeComments(stri):
    nstri = ""
    for i in stri:
        if i == ";":
            return nstri
        nstri+=i
    return nstri
def getComments(stri):
    loc = stri.find(";")
    if loc==-1:
        return ""
    if loc==0:
        return stri
    return stri[loc:]
class command:
    def __init__(self,stri):
        self.original = stri
        self.pointer = getRef(stri)
        self.inst = getInst(stri)
        self.args = getArgs(stri)
        self.com = getComments(stri)
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
        for subArg in self.args:
            newStr+=",".join(subArg) + " "
        if self.com!="":
            newStr+=self.com
        return newStr
    def replace(self,replace,replacement):
        for i in range(len(self.args)):
            for ii in range(len(self.args[i])):
                if self.args[i][ii]==replace:
                    self.args[i][ii] = replacement
    def copy(self):
        new = command(self.rebuild())
        return new
    def formatLine(self,space=[10,10,10]):
        newLine = ""
        count = 0
        if self.pointer!="":
            newLine+=pad(self.pointer+":",space[count])
        else:
            newLine+=" "*space[count]
        if len(space)-1>count:
            count+=1
        if self.inst=="":
            return newLine + self.com
        newLine+=pad(self.inst,space[count])
        if len(space)-1>count:
            count+=1
        for i in self.args:
            newLine+=pad(",".join(i),space[count])
            if len(space)-1>count:
                count+=1
        newLine+=self.com
        return newLine

