import pep9lib
import os
class pepAdvancedFileHandler:
    def __init__(self,folderCheck):
        self.fslist = folderCheck
    def handleFiles(self,fileName):
        for folder in self.fslist:
            if fileName in os.listdir(folder):
                print(folder + "\\" + fileName)
                with open(folder + "\\" + fileName,"r") as file:
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