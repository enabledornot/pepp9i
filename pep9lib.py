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
    split = splitArgs(cmd)
    if len(split)==0 or len(split[0])==0:
        return ""
    if split[0][-1]==":":
        return split[0][:-1]
    return ""
def getInst(cmd):
    split = splitArgs(cmd)
    if len(split)==0 or len(split[0])==0:
        return ""
    if split[0][-1]==":":
        split.pop(0)
    if len(split)==1:
        return ""
    return split[1]
def getArgs(cmd):
    split = splitArgs(cmd)
    if len(split)==0 or len(split[0])==0:
        return []
    if split[0][-1]==":":
        split.pop(0)
    if len(split)<=1:
        return []
    return split[1].split(",")
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
    return stri[loc:]