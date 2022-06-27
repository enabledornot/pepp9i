import pep9lib
def resolveCollisions(code):
    global globalVars
    global usedVars
    global colCount
    globalVars = []
    usedVars = []
    colCount = 0
    for line in code:
        if line.inst==".GLOBAL":
            globalVars.append(line.args[0][0])
    resolveCollisionsRec(code,0)
def resolveCollisionsRec(code,lineNumb):
    count = lineNumb
    localVars = {}
    resolveAhead(code,count,localVars)
    while len(code)>count and not code[count].getBeginCom()=="}":
        if code[count].getBeginCom()=="{":
            count = resolveCollisionsRec(code,count+1)
        else:
            resolveLineArgs(code[count],localVars)
        count+=1
    return count
def resolveAhead(code,count,localVars):
    window = 0
    for line in code[count:]:
        if line.getBeginCom()=="{":
            window+=1
        if line.getBeginCom()=="}":
            window-=1
        if window==0:
            resolveLine(line,localVars)
        if window==-1:
            break
def resolveLine(command,localVars):
    global usedVars
    global globalVars
    global colCount
    if command.pointer!="":
        if (command.pointer not in globalVars):
            if(command.pointer in usedVars):
                localVars[command.pointer] = "ZZ"+str(colCount)
                command.pointer = localVars[command.pointer]
                colCount+=1
            else:
                usedVars.append(command.pointer)
def resolveLineArgs(command,localVars):
    if len(command.args)==0:
        return
    arguments = command.args[0]
    for i in range(len(arguments)):
        if arguments[i] in localVars:
            arguments[i] = localVars[arguments[i]]

