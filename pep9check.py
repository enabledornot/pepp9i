with open("pep9inst.txt","r") as f:
    pep9inst = f.read().splitlines()
def instCheck(instruction):
    global pep9inst
    for i in pep9inst:
        if instruction.startswith(removeUpper(i)):
            return True
    return False
def removeUpper(stri):
    tmp = ""
    for i in stri:
        if i.isUpper():
            tmp+=i
    return tmp