import pep9lib
class pepAdvancedFileHandler:
    def read(self,filename,args):
        try:
            with open(filename,"r") as file:
                code = file.read().split("\n")
        except:
            args['parent'].error("File Not Found error")
            return [pep9lib.command(";FILE NOT FOUND ERROR")]
        newCode = []
        count = 0
        for line in code:
            newCode.append(pep9lib.command(line,lineNumb=count,fileName=filename,parentCommand=args['parent']))
            count+=1
        return newCode