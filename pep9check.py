with open("pep9inst.txt","r") as f:
    pep9inst = f.read().splitlines()
def instCheck(instruction):
    global pep9inst
    for i in pep9inst:
        if i[:len(instruction)]==instruction:
            return True
    return False