# IMPORTS
from pep9lib import splitArgs
import pep9check
# GLOBAL VARS
appendd = []
macroList = {}
# METHODS
def compile(filename):
    # resets global variables
    global appendd
    global macroList
    appendd = []
    macroList = {}
    # Compiles code with appends and includes
    rslt = compileRec(readCodeFile(filename))
    rslt.append(";begin append")
    for i in appendd:
        insertFileIntoList(rslt,i)
    rslt.append(";end\nnoend:     STOP\n.END")
    # Handle collision
    resolveCollisions(rslt)
    # Exports
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
        if len(split[0])==0 or split[0][0]==";":
            ndata.append(line)
            continue
        if split[0]==".INCLUDE":
            insertFileIntoList(ndata, split[1][1:-1])
        elif split[0]==".APPEND":
            appendd.append(split[1][1:-1])
        elif split[0]==".GLOBAL":
            ndata.append(line)
        elif split[0]==".END":
            ndata.append("     BR     noend")
        else:
            pointer = ""
            if split[0][-1]==":":
                pointer = split.pop(0)
            if split[0][0]!="." and not pep9check.instCheck(split[0]):
                if split[0] in macroList:
                    injectedMacro = injectArguments(split)
                    if pointer!="":
                        ndata.append(pointer + "     NOP0;")
                    insertIntoList(ndata,injectedMacro)
                else:
                    print("INVALID INSTRUCTION {}".format(split[0]))
                    ndata.append(";;INVALID MACRO {}".format(split[0]))
            else:
                ndata.append(line)

    return ndata
colCount = 0
def resolveCollisions(code):
    global colCount
    global colList
    colCount = 0
    colList = []
    for i in code:
        split = splitArgs(i)
        if split[0]==".GLOBAL":
            colList.append(split[1])
    resolveCollisionsRec(code,0)
def resolveCollisionsRec(code,starting):
    global colCount
    global colList
    count = starting
    localCollisions = {}
    while len(code)>count and (len(code[count])<2 or code[count][:2]!=";}"):
        if code[count][:2]==";{":
            count+=1
            count = resolveCollisionsRec(code,count)
        else:
            split = splitArgs(code[count])
            if split[0]==".GLOBAL":
                localCollisions[split[1]] = split[1]
                code[count] = ";" + code[count]
            vars = extractAllVars(code[count])
            if len(vars)>0:
                for varName in vars:
                    print(varName)
                    if varName not in localCollisions:
                        if varName in colList:
                            localCollisions[varName] = "ZZ"+str(colCount)
                            colCount+=1
                        else:
                            localCollisions[varName] = varName
                            colList.append(varName)
                    code[count] = varReplace(code[count],varName,localCollisions[varName])
        count+=1
    return count
def varReplace(command, mat, rep):
    if mat==rep:
        return command
    print(command)
    print(mat)
    print(rep)
    print("-")
    split = splitArgs(command)
    if len(split)==0:
        return command
    if split[0][-1]==":":
        if split[0][:-1]==mat:
            command = command.replace(split[0],rep+":")
        split.pop(0)
    if len(split)<2:
        return command
    newArgs = split[1].split(",")
    if newArgs[0]==mat:
        newArgs[0]=rep
    command = command.replace(split[1],','.join(newArgs))
    return command
def extractAllVars(cmdStr):
    split = splitArgs(cmdStr)
    vars = []
    if len(split)==0:
        return vars
    if len(split[0])==0:
        return vars
    if split[0][-1]==":":
        vars.append(split[0][:-1])
        split.pop(0)
    if len(split)<2:
        return vars
    if split[1].split(",")[0].isdigit() or split[1][0]=="\"":
        return vars
    vars.append(split[1].split(",")[0])
    return vars
    
def extractVar(cmdstr):
    splitUp = splitArgs(cmdstr)
    if len(splitUp[0])==0 or splitUp[0][0]==";":
        return ""
    if splitUp[0][-1]==":":
        return splitUp[0][:-1]
    return ""
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
            else:
                macroArgs = []
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
def insertFileIntoList(blist,ntoc):
    blist.append(";{ " + ntoc)
    insertIntoList(blist,readCodeFile(ntoc))
    blist.append(";} " + ntoc)
def insertIntoList(blist,code):
    ncompile = compileRec(code)
    for j in ncompile:
        blist.append(j)