import sys
import pep9icl
import args2json
import pepfs
import os
args = args2json.parse(sys.argv)
# handle arguments
if "-help" in args or 1 not in args:
    print("{} <program.pep2> [-includeBlank] [-removeComments]".format(args[0]))
    quit()
if "-includeBlank" in args:
    removeEmpty = False
else:
    removeEmpty = True
if "-removeComments" in args:
    removeAllComments = True
else:
    removeAllComments = False
fshandler = pepfs.pepAdvancedFileHandler([os.getcwd()])
ci = pep9icl.pep9i(removeEmptyLines=removeEmpty,removeAllOriginalComments=removeAllComments,fileHandler=fshandler)
print("compiling {} with {}".format(args[1],ci.version))
ci.compile(os.getcwd()+"\\"+args[1])