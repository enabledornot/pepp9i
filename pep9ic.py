import sys
import pep9icl
import args2json
import pepfs
args = args2json.parse(sys.argv)
# handle arguments
if "-help" in args or 1 not in args:
    print("{} <program.pep2> [-includeBlank] [-includeComments]".format(args[0]))
    quit()
if "-includeBlank" in args:
    removeEmpty = True
else:
    removeEmpty = False
if "-includeComments" in args:
    removeAllComments = True
else:
    removeAllComments = False
fshandler = pepfs.pepAdvancedFileHandler()
ci = pep9icl.pep9i(removeEmptyLines=removeEmpty,removeAllOriginalComments=removeAllComments,fileHandler=fshandler)
print("compiling {} with {}".format(args[1],ci.version))
ci.compile(args[1])