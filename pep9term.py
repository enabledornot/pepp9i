import os
import shutil
def compilel(pepSource):
    if not os.path.isdir("_TMP"):
        os.mkdir("_TMP")
    os.system("pep9term asm -s {} -o _TMP/pep.pepo".format(pepSource))
    compiled = ""
    with open("_TMP/pep.pepl") as k:
        compiled = k.read()
    shutil.rmtree("_TMP")
    return compiled