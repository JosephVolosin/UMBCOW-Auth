'''
    whitelist.py acts as a simple way to interface with the whitelist.
'''

FN = "whitelist.txt"

# write(newAddition) adds newAddition to the whitelist
def write(newAddition):
    print("Writing " + newAddition + " to the whitelist..")
    with open(FN, 'a') as f:
        f.write(newAddition + "\n")
        f.close()
    
# clear() removes all lines from the file
def clear():
    print("Clearing whitelist..")
    f = open(FN, 'w')
    f.close()