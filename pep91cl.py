# IMPORTS
import pep9lib
import pep9check
from pep9col import resolveCollisions
# GLOBAL VARS
appendd = []
macroList = {}
# METHODS
def compile(filename):
    # resets global variables
    global appendd
    global macroList
    global prevFiles
    appendd = []
    macroList = {}
    prevFiles = []
    # Compiles code with appends and includes
    rslt = compileRec(readCodeFile(filename))
    rslt.append(pep9lib.command(";begin append"))
    while len(appendd)!=0:
        insertFileIntoList(rslt,appendd.pop(0))
    rslt.append(pep9lib.command(";end"))
    rslt.append(pep9lib.command("noend:     STOP"))
    rslt.append(pep9lib.command(".END"))
    # Handle collision
    resolveCollisions(rslt)
    # Exports
    nfile = ";compiled by python.pep91.v1\n"
    for i in rslt:
        nfile+=i.formatLine()+"\n"
    with open("PEPP.pep","w") as f:
        f.write(nfile)
def readCodeFile(filename):
    global prevFiles
    if filename in prevFiles:
        return []
    prevFiles.append(filename)
    with open(filename,"r") as f:
        rdata = f.read().split("\n")
    ncode = []
    for i in rdata:
        ncode.append(pep9lib.command(i))
    return ncode
def compileRec(code):
    global appendd
    global macroList
    fdata = extractMacros(code)
    ndata = []
    for line in fdata:
        if line.inst==".INCLUDE":
            insertFileIntoList(ndata, line.args[0][0][1:-1])
        elif line.inst==".APPEND":
            appendd.append(line.args[0][0][1:-1])
        elif line.inst==".GLOBAL":
            ndata.append(line)
        elif line.inst==".END":
            ndata.append(pep9lib.command("     BR     noend"))
        else:
            if len(line.inst)!=0 and line.inst[0]!="." and not pep9check.instCheck(line.inst):
                if line.inst in macroList:
                    injectedMacro = injectArguments(line)
                    if line.pointer!="":
                        ndata.append(pep9lib.command(line.pointer+":" + "     NOP0;"))
                    insertIntoList(ndata,injectedMacro)
                else:
                    print("INVALID INSTRUCTION {}".format(line.inst))
                    ndata.append(";;INVALID MACRO {}".format(line.inst))
            else:
                ndata.append(line)

    return ndata
colCount = 0
def extractVar(cmdstr):
    splitUp = pep9lib.splitArgs(cmdstr)
    if len(splitUp[0])==0 or splitUp[0][0]==";":
        return ""
    if splitUp[0][-1]==":":
        return splitUp[0][:-1]
    return ""
def injectArguments(line):
    global macroList
    macro = macroList[line.inst]
    macInst = []
    for mLine in macro["inst"]:
        macInst.append(mLine.copy())
    if len(macro["args"])>0:
        macArgs = line.args[0]
    cnt = 0
    for i in macro["args"]:
        for ii in range(len(macInst)):
            macInst[ii].replace(i,macArgs[cnt])
        cnt+=1
    return macInst
def extractMacros(fdata):
    global macroList
    macroName = ""
    macroInstructions = []
    macroArgs = []
    nfdata = []
    for line in fdata:
        if line.inst==".MACRO":
            macroName = line.args[0][0]
            if len(line.args)>1:
                macroArgs = line.args[1]
            else:
                macroArgs = []
            macroInstructions = [pep9lib.command(";;" + macroName)]
        elif line.inst==".MACROEND":
            macroList[macroName] = {
                "args":macroArgs,
                "inst":macroInstructions
            }
            macroName = ""
        else:
            if macroName=="":
                nfdata.append(line)
            else:
                macroInstructions.append(line)
    return nfdata
def insertFileIntoList(blist,ntoc):
    blist.append(pep9lib.command(";{ " + ntoc))
    insertIntoList(blist,readCodeFile(ntoc))
    blist.append(pep9lib.command(";} " + ntoc))
def insertIntoList(blist,code):
    ncompile = compileRec(code)
    for j in ncompile:
        blist.append(j)