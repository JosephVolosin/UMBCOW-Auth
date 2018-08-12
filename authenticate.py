# authenticate.py handles the code for making a search request to the UMBC
#   directory
# Using urllib bc i don't know how to use other things idk what would
#   work best in this situation
import requests

''' Constants '''
DIRECTORY_URL = "https://www.umbc.edu/search/directory/?search="

'''
 authenticateUser() attempts to authenticate a user
 Input:
    userMsg     = string, user's username or ID
 Output:
    0 = Fail
    1 = Success
    2 = Further contact needed
'''
def authenticateUser(userMsg):

    userMsg = userMsg[userMsg.find(" ") + 1:]
    print(userMsg)
    url = DIRECTORY_URL + userMsg
    resp = requests.get(url)
    # Check that UMBC website is available
    if(checkAvailable() == False):
        return 0
     # Checks that search was valid
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Server could not be contacted, status code '" +
                str(resp.status_code))
    # Search results
    if (any(char.isdigit() for char in userMsg) and
            ('1 result found' in resp.text)):
        return 1
    else:
         return 0

'''
 checkExistingAuth() checks the whitelist for the user's given username/ID
 Input:
    userName    = string, user's discord tag
    userMsg     = string, user's username or ID
 Output:
    0 = Exists in whitelist
    1 = Doesn't exist in whitelist
    2 = Discord account is already authenticated
'''
def checkExistingAuth(userName, userMsg):

    userMsg = userMsg[userMsg.find(" ") + 1:]
    try:
        whitelist = open('whitelist.txt')
    except:
        print("Whitelist could not be opened.")
        return 0 # TODO - change this return to be it's own number
    for l in whitelist.readlines():
        if(userName in l):
            print("Your discord account is already authenticated.")
            return 2
        elif(userMsg in l):
            # TODO - Bot needs to message officers when it receives '2'
            print("You have already used that e-mail/campus ID to authenticate \
                    an account. A request will be sent to admins for furthur \
                    review.")
            return 0
    return 1

'''
 checkAvailable() checks if the UMBC website is available right now
 Input:
    None
 Output:
    True/False on if website is available
'''
def checkAvailable():

    if(requests.get(DIRECTORY_URL).status_code == 200):
        return True
    else:
        return False