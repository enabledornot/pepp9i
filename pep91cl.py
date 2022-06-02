
def compile(filename):
    rslt = compileRec(filename)
    nfile = ";compiled by python.pep91.v1\n"
    for i in rslt:
        nfile+=i+"\n"
    with open("PEPP.pep","w") as f:
        f.write(nfile)

def compileRec(filename):
    with open(filename,"r") as f:
        fdata = f.read().split("\n")
    ndata = []
    for i in range(len(fdata)):
        poi = fdata[i].find(".INCLUDE")
        if poi!=-1:
            ntoc = findQuotedDataAfter(poi,fdata[i])
            ndata.append(";{ " + ntoc)
            ncompile = compileRec(ntoc)
            for j in ncompile:
                ndata.append(j)
            ndata.append(";} " + ntoc)
        else:
            ndata.append(fdata[i])

    return ndata
def findQuotedDataAfter(pos,strt):
    indata = ""
    prevBak = False
    inQuotes = False
    for i in strt:
        if prevBak:
            if inQuotes:
                indata+=i
        else:
            if i=="\"":
                inQuotes = not(inQuotes)
            else:
                if inQuotes:
                    indata+=i
        pos+=1
    return indata