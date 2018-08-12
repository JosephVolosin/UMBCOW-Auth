'''
    visitor.py acts as a simple way to interface with the visitors.txt file
    Entry format: <discord-member>,<discord-visitor>,<timestamp>
'''
import datetime

FN = "visitors.txt"
TIME_PATTERN = "%Y%m%d %H:%M:%S"

# removeOldVisitors() removes all visitors that have an age of more than a day
def removeOldVisitors():

    now_time_stamp = datetime.datetime.now()
    now_time_stamp = datetime.datetime.strftime(now_time_stamp, TIME_PATTERN)
    f = open(FN, 'r')
    for l in f:
        l_temp = l.split(",")[2].rstrip()
        print(l_temp)
        cur_dt = datetime.datetime.strptime(l_temp, TIME_PATTERN)
        cur_dt += datetime.timedelta(hours=24)
        now_dt = datetime.datetime.strptime(now_time_stamp, TIME_PATTERN)
        if(cur_dt < now_dt):
            remove(l)
            print("\tRemoving line:")
            print("\t\t" + l)

# write(newAddition) adds newAddition to the visitors file
def write(newAddition):

    cur_time_stamp = datetime.datetime.now()
    cur_time_stamp = datetime.datetime.strftime(cur_time_stamp, TIME_PATTERN)

    # Capture all old lines to be re-written
    old_lines = ''
    with open(FN, 'r') as f:
        for l in f:
            old_lines += l + "\n"
        f.close()

    # Write all lines
    with open(FN, 'w') as f:
        f.write(old_lines)
        f.write(newAddition + "," + cur_time_stamp + "\n")
        f.close()

# remove(removal) removes whatever removal is
def remove(removal):

    with open(FN, 'r') as f:
        full_lines = f.readlines()
    try:
        full_lines.remove(removal)
    except:
        print("\tThe removal wasn't found in the visitors file.")
    clear()
    with open(FN, 'w') as f:
        f.write(full_lines)

# checkExistingVisitor(name) checks if the visitor is already checked in with the visitors file
# True  = Visitor is checked in already
# False = Visitor is not currently checked in
def checkExistingVisitor(name):
    with open(FN, 'r') as f:
        lines = f.readlines()
        if(name in lines):
            return True
    return False

# clear() removes all lines from the file
def clear():

    f = open(FN, 'w')
    f.close()