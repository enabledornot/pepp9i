import pep9lib
class pepAdvancedFileHandler:
    def read(self,filename,args):
        with open(filename,"r") as file:
            code = file.read().split("\n")
        return code