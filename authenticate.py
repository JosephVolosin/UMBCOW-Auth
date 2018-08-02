# authenticate.py handles the code for making a search request to the UMBC
#   directory
# Using urllib bc i don't know how to use other things idk what would
#   work best in this situation
import requests

# This is the base URL for searches, the URL changes to 
#   DIRECTORY_URL + ?search='search here' when used, so just concat it and
#   run another request
#   ?search=josephv2%40umbc.edu is the URL when you search my e-mail, however
#   it seems like feeding it '@' instead of '%40' gives the same results
DIRECTORY_URL = "https://www.umbc.edu/search/directory/?search="

# checkUMBCStatus() sends a request to the website to show that it's available
# Input:
#   None
# Output:
#   0 = Fail
#   1 = Success
#   2 = Further contact needed
def checkUMBCStatus(userMsg):
    url = DIRECTORY_URL + userMsg
    try:
        response = requests.get(url)
    except:
        print("Could not reach server.")
        return 0 # This needs to have a error message that gets sent to the user
    # Valid ID
    if any(char.isdigit() for char in userMsg) and '1 result found' in response.text:
        #TODO remove the non-verified role
        return 1
    elif '@' in userMsg:
        return 2
    else:
        return 0

'''
 checkExistingAuth(userName, userMsg) checks to see if the given userName or use
 userMsg (containing an e-mail or campus ID) exist in the whitelist.
 
 Input:
    userName    = string, user's Discord name
    userMsg     = string, user's inputted UMBC campus ID/email
 Output:
    0           = Failure
    1           = Pass, not in whitelist
    2           = Already used e-mail/ID
    3           = Discord account already authenticated
'''
def checkExistingAuth(userName, userMsg):
    try:
        whitelist = open("whitelist.txt")
    except:
        print("Whitelist could not be opened, is it in this dir?")
        return 0
    for l in whitelist.readlines():
        if (userName in l):
            print("You have already authenticated this account.. Why are you doing it again?")
            return 3
        elif (userMsg in l):
            print("You have already used that e-mail/campus ID to authenticate an account. A request will be sent to an admin to manuall authenticate.")
            return 2
    return 1

'''
 validateUserMsg(userMsg) validates the user's message to make sure it either
 appears that it's a valid UMBC e-mail or campus ID.
 
 Input:
    userMsg     = string, user's message on Discord of their e-mail/ID
 Output:
    0           = Fail, not valid looking
    1           = Pass, valid
'''
def validateUserMsg(userMsg):
    # Check for e-mail
    if ('@umbc.edu' in userMsg):
        return 1
    # Check for Campus ID TODO - Have this validate the form rather than len
    if len(userMsg) == 7:
        return 1
    # Else, fail
    return 0
