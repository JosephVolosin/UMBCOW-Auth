# authenticate.py handles the code for making a search request to the UMBC
#   directory
# Using urllib bc i don't know how to use other things idk what would
#   work best in this situation
import urllib
from urllib import request

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
        await 1
    elif '@' in userMsg:
        return 2
    else:
        return 0
