# discord.py houses the code for the Discord bot that will run on the server.
# This file uses discord-keys.txt which houses the Discord API keys, this file
#   is hidden for security.
import authenticate, discord
try:    
    with open('discord-keys.txt') as f:
        API_KEYS = f.readlines()
except:
    print("'discord-keys.txt' was not found. Please make sure it's located" +
        " in the current directory.")
    exit()

def main():
    print("Blah")

main()