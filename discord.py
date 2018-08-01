# discord.py houses the code for the Discord bot that will run on the server.
# This file uses discord-keys.txt which houses the Discord API keys, this file
#   is hidden for security.
import authenticate, discord, asyncio, aiohttp
from discord import Game
from discord.ext.commands import Bot

'''
Constants
'''
BOT_PREFIX = ('?', '!')
TOKEN = fetchToken()
SERVER_ID = '360868374244491264'
CLIENT = Bot(command_prefix=BOT_PREFIX)

''' Helper Methods '''
def fetchToken()
    # assuming that this is running in the same dir. as discord-keys.txt
    try:
        with open('discord-keys.txt') as f:
            return f.readlines()[0]
    else:
        print("Error opening 'discord-keys.txt', FATAL.")
        return 0

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print('Current servers:')
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

''' Bot Methods '''
@client.command(name='setupServer',
                description='sets the server up to use the verification system',
                breif='sets the server up to use the verification system',
                aliases=['setupserver', 'setup', 's'],
                pass_context=True)
async def setupServer(*args):
    #TODO create the non-verified role
    await client.create_role(SERVER_ID, name='NotVerified')
    await client.say('Created a NotVerified role')
    #TODO make the user hide all channels to the non-verified role
    await client.say('Make sure to set the default non-verified role permissions.')
    #TODO create the new channels needed
    await client.create_channel(SERVER_ID, 'verification', *overwrites, type=discord.ChannelType.text)
    await client.create_channel(SERVER_ID, 'verification-admins-only', *overwrites type=discord.ChannelType.text)


@client.command(name='setAllNotVerified',
		description='setsall users in the server to a NotVerified role',
		breif='sets all users in the server to a NotVerified role',
		aliases=['setANV','fukAllYall'],
		pass_context=True)
#TODO make a !setallNotVerified command so that it gives all users a non-verified role
async def setAllNotVerified(*args):
	role = discord.utils.get(args[0].server.roles, name='NotVerified')
	serverMembers = args.server.members
	for member in serverMembers:
		await client.add_roles(member, role)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name='!verify for help'))
    print('Logged in as ' + CLIENT.user.name)

#TODO: overwrite discord.on_member_join
@client.command(name='verify',
		description='checks to see if a user is a valid UMBC student',
		breif='Verify yourself to allow access to this discord server',
		aliases=['v','verifyme','verifyMe','VerifyMe','Verify'],
		pass_context=True)

''' Run '''
if __name__ == '__main__':
    client.loop.create_task(list_servers())
    if(TOKEN == 0):
        print("Token was not found, therefore bot can't run.")
        exit()
    else:
        client.run(TOKEN)