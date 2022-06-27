import pep9lib
def resolveCollisions(code):
    global globalVars
    global usedVars
    global colCount
    globalVars = []
    usedVars = []
    colCount = 0
    # newCMD = []
    # for i in code:
    #     for ii in i.split("\n"):
    #         newCMD.append(pep9lib.command(ii))
    #         print(newCMD[-1])
    #         if newCMD[-1].inst==".GLOBAL":
    #             globalVars.append(newCMD[-1].args[0])
    #             newCMD[-1] = pep9lib.command(";"+ii)
    for line in code:
        if line.inst==".GLOBAL":
            globalVars.append(line.args[0][0])
    resolveCollisionsRec(code,0)
    # for i in range(len(code)):
    #     code[i] = newCMD[i].__str__()
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
    for i in range(len(command.args)):
        if command.args[i] in localVars:
            command.args[i] = localVars[command.args[i]]

