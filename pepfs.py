import pep9lib
class pepAdvancedFileHandler:
    def read(self,filename,args):
        with open(filename,"r") as file:
            code = file.read().split("\n")
        newCode = []
        count = 0
        for line in code:
            newCode.append(pep9lib.command(line,lineNumb=count,fileName=filename))
            count+=1
        return newCode