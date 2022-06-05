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
            ndata.append(";"+line)
        elif split[0]==".END":
            ndata.append("     BR     noend")
        else:
            if split[0][-1]==":":
                split.pop(0)
            if split[0][0]!="." and not pep9check.instCheck(split[0]):
                if split[0] in macroList:
                    injectedMacro = injectArguments(split)
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
            varName = extractVar(code[count])
            if varName!="":
                if varName not in localCollisions:
                    if varName in colList:
                        localCollisions[varName] = "ZZ"+str(colCount)
                        colCount+=1
                    else:
                        localCollisions[varName] = varName
                        colList.append(varName)
                code[count] = code[count].replace(varName,localCollisions[varName],1)
        count+=1
    return count
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