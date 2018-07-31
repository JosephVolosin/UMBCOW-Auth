# authenticate.py handles the code for making a search request to the UMBC
#   directory
# Using urllib bc i don't know how to use other things idk what would
#   work best in this situation
from urllib import request

# This is the base URL for searches, the URL changes to 
#   DIRECTORY_URL + ?search='search here' when used, so just concat it and
#   run another request
#   ?search=josephv2%40umbc.edu is the URL when you search my e-mail, however
#   it seems like feeding it '@' instead of '%40' gives the same results
DIRECTORY_URL = "https://www.umbc.edu/search/directory/"

# checkUMBCStatus() sends a request to the website to show that it's available
# Input:
#   None
# Output:
# 0/1 for Fail/Pass on website being up or not
def checkUMBCStatus():
    try:
        request.urlopen(DIRECTORY_URL)
        return 1
    except urllib.error.HTTPError:
        print("UMBC website was unreachable.")
    return 0