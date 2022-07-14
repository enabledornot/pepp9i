# A python add-on that converts command line arguments into a dictionary style object
# Expects an already separated argument list like what is provided by sys.argv
def parse(args):
    rslt = {}
    current = ""
    count = 0
    for arg in args:
        if arg[0]=="-":
            current = arg
            rslt[current] = []
        elif current=="":
            rslt[count] = arg
            count+=1
        else:
            rslt[current].append(arg)
    return rslt