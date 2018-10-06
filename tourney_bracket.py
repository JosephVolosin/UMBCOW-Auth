'''
    tourney_bracket.py handles the functions of the !bracket command
    update(newLink) - Updates bracket.txt to have newest bracket link and the date it was updated
    output()        - Fetches the newest bracket link and sends it back to umbc-bot.py
'''
from datetime import date

FN = "bracket.txt"

def update(newLink):

    date_current = date.today().strftime("%d/%m/%Y")
    with open(FN, 'w') as f:
        f.write("Bracket: " + newLink + " (Updated: " + date_current + ")")

def output():

    with open(FN) as f:
        return f.readline()