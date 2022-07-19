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
            if folder.search(fileName):
                with open(folder.name + "\\" + fileName,"r") as file:
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
        list = os.listdir(folderName)
        self.name = folderName
        self.files = []
        for file in list:
            if os.path.isfile(folderName + "\\" + file):
                self.files.append(file.lower())
    def search(self,string):
        if string.lower() in self.files:
            return True
        return False