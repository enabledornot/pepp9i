from fileinput import filename
import pep9lib
import os
class pepAdvancedFileHandler:
    def __init__(self,folderCheck):
        self.fslist = folderCheck
        self.folders = []
        for folder in self.fslist:
            self.folders.append(importFolder(folder))
    def handleFiles(self,fileName):
        for folder in self.folders:
            ext = getext(fileName)
            if ext=="pep1" or ext=="pep2":
                searched = folder.deepSearch(fileName)
            else:
                searched = folder.search(fileName)
            if searched!="":
                with open(searched) as file:
                    code = file.read().split("\n")
                return code
    def read(self,filename,args):
        code = self.handleFiles(filename)
        if code==None:
            args['parent'].error("File import error")
            return []
        newCode = []
        count = 0
        for line in code:
            newCode.append(pep9lib.command(line,lineNumb=count,fileName=filename,parentCommand=args['parent']))
            count+=1
        return newCode
class importFolder:
    def __init__(self,folderName):
        self.name = folderName
        self.files = []
        explore(folderName,self.files)
    def deepSearch(self,key):
        if isPath(key):
            return key
        for file in self.files:
            base = os.path.basename(file)
            if base==key.lower():
                return file
        return ""
    def search(self,key):
        if isPath(key):
            newPath = path(pathName=key)
        else:
            newPath = path(pathName=self.name+"\\"+key)
        rslt = newPath.locate()
        return rslt
def explore(path,list):
    if os.path.isfile(path):
        list.append(path.lower())
        return
    if os.path.isdir(path) and checkPath(path):
        for newPath in os.listdir(path):
            explore(path + "\\" + newPath,list)
def checkPath(path):
    base = os.path.basename(path)
    if len(base)==0 or base[0]=="_" or base[0]==".":
        return False
    return True
def isPath(path):
    return len(path)>1 and (path[1]==":" or path[0]=="\\")
def getext(path):
    return path.split(".")[-1]
class path:
    def __init__(self,pathName=None,pathHead=None,pathTail=None):
        if pathHead!=None:
            self.folder = pathHead
            self.file = pathTail
            return
        head,tail = os.path.split(pathName)
        self.folder = head.split("\\")
        self.file = tail.split(".")
    def toStr(self):
        return "\\".join(self.folder)+"\\"+".".join(self.file)
    def getFolder(self):
        return "\\".join(self.folder)
    def shift(self):
        self.folder.append(self.file.pop(0))
    def deshift(self):
        self.file.insert(0,self.folder.pop(-1))
    def locate(self):
        while os.path.isdir(self.getFolder()):
            if os.path.isfile(self.toStr()):
                return self.toStr()
            self.shift()
        self.deshift()
        print(self.toStr())
        if os.path.isfile(self.toStr()):
            return self.toStr()
        if len(self.file)==0:
            return self.getFolder()
        return ""