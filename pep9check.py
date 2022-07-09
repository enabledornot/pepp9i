with open("pep9inst.txt","r") as f:
    pep9inst = f.read().splitlines()
def instCheck(instruction):
    global pep9inst
    for i in pep9inst:
        if instruction.startswith(removeLower(i)) and len(i)==len(instruction):
            return True
    return False
def removeLower(stri):
    tmp = ""
    for i in stri:
        if not(i.islower()):
            tmp+=i
    return tmp