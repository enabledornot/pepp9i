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