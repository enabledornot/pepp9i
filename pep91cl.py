appendd = []
macroList = {}
def compile(filename):
    global appendd
    global macroList
    appendd = []
    macroList = {}
    rslt = compileRec(readCodeFile(filename))
    rslt.append(";begin append")
    for i in appendd:
        insertFileIntoList(rslt,i)
    nfile = ";compiled by python.pep91.v1\n"
    for i in rslt:
        nfile+=i+"\n"
    with open("PEPP.pep","w") as f:
        f.write(nfile)
def readCodeFile(filename):
    with open(filename,"r") as f:
        rdata = f.read().split("\n")
    return rdata
def compileRec(code):
    global appendd
    global macroList
    fdata = extractMacros(code)
    ndata = []
    for line in fdata:
        split = splitArgs(line)
        if split[0]==".INCLUDE":
            insertFileIntoList(ndata, split[1][1:-1])
        elif split[0]==".APPEND":
            appendd.append(split[1][1:-1])
        elif split[0]==".GLOBAL":
            continue
        else:
            if split[0]!="" and split[0][0]!=";":
                if split[0][-1]==":":
                    split.pop(0)
                if split[0] in macroList:
                    for i in injectArguments(split):
                        ndata.append(i)
                else:
                    ndata.append(line)

    return ndata
def injectArguments(splitInst):
    global macroList
    macro = macroList[splitInst[0]]
    macInst = macro["inst"]
    if len(macro["args"])>0:
        macArgs = splitInst[1].split(",")
    cnt = 0
    for i in macro["args"]:
        for ii in range(len(macInst)):
            macInst[ii] = macInst[ii].replace(i,macArgs[cnt])
        cnt+=1
    return macInst
def extractMacros(fdata):
    global macroList
    macroName = ""
    macroInstructions = []
    macroArgs = []
    nfdata = []
    for line in fdata:
        split = splitArgs(line)
        if split[0]==".MACRO":
            macroName = split[1]
            if len(split)>2:
                macroArgs = split[2].split(",")
            macroInstructions = [";;" + macroName]
        elif split[0]==".MACROEND":
            macroList[macroName] = {
                "args":macroArgs,
                "inst":macroInstructions
            }
            macroName = ""
        else:
            if macroName=="":
                nfdata.append(line)
            else:
                if len(line)!=0 and line[0]!=";":
                    macroInstructions.append(line)
    return nfdata
def splitArgs(stri):
    args = [""]
    for i in stri:
        if i==" ":
            if args[-1]!="":
                args.append("")
        else:
            args[-1]+=i
    return args
def insertFileIntoList(blist,ntoc):
    blist.append(";{ " + ntoc)
    insertIntoList(blist,readCodeFile(ntoc))
    blist.append(";} " + ntoc)
def insertIntoList(blist,code):
    ncompile = compileRec(code)
    for j in ncompile:
        blist.append(j)
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