# General library for dealing with pep9 assembly in python


import copy

def splitArgs(stri,splitChar=" "):
    args = [""]
    count = 0
    while count<len(stri):
        if stri[count] in ["'","\""]:
            stopChar = stri[count]
            args[-1]+=stri[count]
            count+=1
            while count<len(stri) and stri[count]!=stopChar:
                args[-1]+=stri[count]
                count+=1
            if count<len(stri):
                args[-1]+=stri[count]
                count+=1
        elif stri[count]==";":
            return args
        else:
            if stri[count]==splitChar:
                if args[-1]!="":
                    args.append("")
            else:
                args[-1]+=stri[count]
            count+=1
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
def pad(stri,leng,chart=' '):
    return stri + (leng-len(stri))*chart
def removeComments(stri):
    nstri = ""
    spaces = ""
    for char in stri:
        if char == ";":
            return nstri
        elif char == " ":
            spaces+=" "
        else:
            nstri+=spaces + char
        spaces = ""
    return nstri
def getComments(stri):
    loc = stri.find(";")
    if loc==-1:
        return ""
    if loc==0:
        return stri
    return stri[loc:]
class command:
    def __init__(self,stri,lineNumb=None,fileName=None,parentCommand=None):
        self.original = stri
        self.extractData(stri)
        self.line = lineNumb
        self.file = fileName
        self.parent = parentCommand
        self.comLineAfter = False
    def extractData(self,stri):
        self.pointer = ""
        self.inst = ""
        self.args = []
        self.com = getComments(stri)
        split = splitArgs(stri)
        if len(split)==0 or len(split[0])<2:
            return
        if split[0][-1]==":":
            self.pointer = split.pop(0)[:-1]
        if len(split)==0:
            return
        self.inst = split[0]
        if len(split)==1:
            return
        args = []
        for i in split[1:]:
            splits = i.split(",")
            if "" in splits:
                splits.remove("")
            args.append(splits)
        self.args = args
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
        new = copy.copy(self)
        new.args = copy.deepcopy(self.args)
        return new
    def formatLine(self,space=[10,10,10]):
        if self.inst=="":
            return self.com
        newList = []
        if self.pointer!="":
            newList.append(self.pointer+":")
        else:
            newList.append("")
        newList.append(self.inst)
        if len(self.args)>0:
            newList.append(",".join(self.args[0]))
        else:
            newList.append("")
        newLine = ""
        if self.comLineAfter:
            newLine = ";"
        newLine+= self.formatList(newList,space=space,allSpaces=self.com!="")
        newLine+=self.com
        return newLine
    def formatList(self,list,space=[10,10,10],allSpaces=False):
        str = ""
        count = 0
        for element in list:
            str+=pad(element,space[count])
            if count<len(space):
                count+=1
        if allSpaces:
            while count<len(space):
                str+=" "*space
                if count<len(space):
                    count+=1
        return str

    def error(self,errorMsg=None):
        if errorMsg!=None:
            print("---- BEGIN ERROR ----")
        if self.parent!=None:
            self.parent.error()
        print("  File {} - Line {}".format(self.file,self.line))
        print("    "+self.formatLine())
        if errorMsg!=None:
            print(errorMsg)
            print ("---- END ERROR ----")
            print("")
class dummyCommand:
    def error(self,errorMsg=None):
        return
