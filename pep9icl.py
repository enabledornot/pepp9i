# IMPORTS
import pep9lib
import pep9check
from pep9col import resolveCollisions
class pep9i:
    def __init__(self):
        self.appendd = []
        self.macroList = {}
        self.prevFiles = []
    def compile(self,filename):
        # Compiles code with appends and includes
        rslt = self.compileRec(self.readCodeFile(filename))
        rslt.append(pep9lib.command(";begin append"))
        while len(self.appendd)!=0:
            self.insertFileIntoList(rslt,self.appendd.pop(0))
        rslt.append(pep9lib.command(";end"))
        rslt.append(pep9lib.command("noend:     STOP"))
        rslt.append(pep9lib.command(".END"))
        # Handle collision
        resolveCollisions(rslt)
        # Exports
        nfile = ";compiled by python.pep9i.v1.1\n"
        for i in rslt:
            nfile+=i.formatLine()+"\n"
        with open("PEPP.pep","w") as f:
            f.write(nfile)
    def readCodeFile(self,filename,parent=None):
        if filename in self.prevFiles:
            return []
        self.prevFiles.append(filename)
        with open(filename,"r") as f:
            rdata = f.read().split("\n")
        ncode = []
        for i in range(len(rdata)):
            ncode.append(pep9lib.command(rdata[i],lineNumb=i,fileName=filename,parentCommand=parent))
        return ncode
    def compileRec(self,code):
        fdata = self.extractMacros(code)
        ndata = []
        for line in fdata:
            if line.inst==".INCLUDE":
                self.insertFileIntoList(ndata, line)
            elif line.inst==".APPEND":
                self.appendd.append(line)
            elif line.inst==".GLOBAL":
                ndata.append(line)
            elif line.inst==".END":
                ndata.append(pep9lib.command("     BR     noend"))
            else:
                if len(line.inst)!=0 and not pep9check.instCheck(line.inst):
                    if line.inst in self.macroList:
                        injectedMacro = self.injectArguments(line)
                        if line.pointer!="":
                            ndata.append(pep9lib.command(line.pointer+":" + "     NOP0;"))
                        self.insertIntoList(ndata,injectedMacro)
                    else:
                        line.error("INVALID INSTRUCTION")
                else:
                    ndata.append(line)

        return ndata
    colCount = 0
    def extractVar(self,cmdstr):
        splitUp = pep9lib.splitArgs(cmdstr)
        if len(splitUp[0])==0 or splitUp[0][0]==";":
            return ""
        if splitUp[0][-1]==":":
            return splitUp[0][:-1]
        return ""
    def injectArguments(self,line):
        macro = self.macroList[line.inst]
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
    def extractMacros(self,fdata):
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
                self.macroList[macroName] = {
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
    def insertFileIntoList(self,blist,importLine):
        ntoc = importLine.args[0][0][1:-1]
        blist.append(pep9lib.command(";{ " + ntoc))
        self.insertIntoList(blist,self.readCodeFile(ntoc,parent=importLine))
        blist.append(pep9lib.command(";} " + ntoc))
    def insertIntoList(self,blist,code):
        ncompile = self.compileRec(code)
        for j in ncompile:
            blist.append(j)