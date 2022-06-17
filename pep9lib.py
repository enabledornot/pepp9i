# General library for dealing with pep9 assembly in python
def splitArgs(stri):
    args = [""]
    for i in stri:
        if i==" ":
            if args[-1]!="":
                args.append("")
        else:
            args[-1]+=i
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
        codeList[count] = formatLine(codeList[count],space=[10,10,10])
        count+=1
def formatLine(codeLine,space=[10,10,10]):
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
    return newLine
def pad(stri,leng,chart=' '):
    return stri + (leng-len(stri))*chart