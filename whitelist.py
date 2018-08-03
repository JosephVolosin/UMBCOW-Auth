FN = "whitelist.txt"

# write(newAddition) adds newAddition to the whitelist
def write(newAddition):
    
    # Capture all old lines to be re-written
    old_lines = ''
    with open(FN, 'r') as f:
        for l in f:
            old_lines += l + "\n"
        f.close()

    # Write all lines
    with open(FN, 'w') as f:
        f.write(old_lines)
        f.write(newAddition + "\n")
        f.close()
    
# clear() removes all lines from the file
def clear():
    f = open(FN, 'w')
    f = close()