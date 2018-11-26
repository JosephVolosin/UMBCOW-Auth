'''
    visitor.py acts as a simple way to interface with the visitors.txt file
    Entry format: <discord-member>,<discord-visitor>,<timestamp>
'''
import datetime

FN = "visitors.txt"
TIME_PATTERN = "%Y%m%d %H:%M:%S"

# removeOldVisitors() removes all visitors that have an age of more than a day
def removeOldVisitors():

    # Create a time of now, as string
    now_time_stamp = datetime.datetime.now()
    now_time_stamp = datetime.datetime.strftime(now_time_stamp, TIME_PATTERN)

    # Compare current visitors checkin times with current time
    f = open(FN, 'r')
    usrs_remove = []
    lines_remove = []
    line_count = 0

    for l in f:
        l_temp = l.split(",")[2].rstrip()
        cur_name = l.split(",")[1]
        cur_dt = datetime.datetime.strptime(l_temp, TIME_PATTERN)
        cur_dt += datetime.timedelta(minutes=1) # Change to hours=24
        now_dt = datetime.datetime.strptime(now_time_stamp, TIME_PATTERN)
        # User is past 24-hour check-in
        if(cur_dt < now_dt):
            lines_remove.append(line_count)
            usrs_remove.append(cur_name)
            # Printout
            print("\tRemoving line:")
            print("\t\t" + l)
            usrs_remove.append(line_count)
        line_count += 1

    f.close()
    removeLines(lines_remove)
    return usrs_remove

# write(newAddition) adds newAddition to the visitors file
def write(newAddition):

    cur_time_stamp = datetime.datetime.now()
    cur_time_stamp = datetime.datetime.strftime(cur_time_stamp, TIME_PATTERN)

    # Write newAddition
    with open(FN, 'a') as f:
        f.write(newAddition + "," + cur_time_stamp + "\n")
        
def removeLines(rm_lines):
    line_count = 0
    final_lines = []
    f = open(FN)
    # Grab
    for l in f.readlines():
        if(line_count not in rm_lines):
            final_lines.append(l)
        line_count += 1
    f.close()
    # Re-write lines
    with open(FN, 'w') as f:
        for l in final_lines:
            f.write(l)

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