# discord.py houses the code for the Discord bot that will run on the server.
# This file uses discord-keys.txt which houses the Discord API keys, this file
#   is hidden for security.
import authenticate, discord, asyncio, aiohttp
from discord.ext.commands import Bot

'''
Constants
'''
BOT_PREFIX = ('?', '!')
SERVER_ID = '455912302202322958'
client = Bot(command_prefix=BOT_PREFIX)

''' Helper Methods '''
# Fetch the bot's token
def fetchToken():
	# assuming that this is running in the same dir. as discord-keys.txt
	try:
		with open('discord-keys.txt') as f:
			for l in f.readlines():
				if('BOT_TOKEN' in l):
					return l[l.find('=') + 1:]
	except:
		print("Error opening 'discord-keys.txt', FATAL.")
		return 0

# List all the servers bot is deployed to
async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print('Current servers:')
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

''' Bot Methods '''
# setupServer() creates the unverified role 
@client.command(name='setupServer',
                description='sets the server up to use the verification system',
                breif='sets the server up to use the verification system',
                aliases=['setupserver', 'setup', 's'],
                pass_context=True)
async def setupServer(*args):
	# Create the 'unverified' role
	server = args[0].message.author.server
	try:
		await client.create_role(server, name='Unverified')
	except:
		quit()
	await client.say('Created a Unverified role')

# setAllNotVerified() gives everyone the unverified role
@client.command(name='setAllNotVerified',
		description='setsall users in the server to a NotVerified role',
		breif='sets all users in the server to a NotVerified role',
		aliases=['setANV','fukAllYall'],
		pass_context=True)
async def setAllNotVerified(*args):
	server = args[0].message.author.server
	role = discord.utils.get(server.roles, name='Unverified')
	serverMembers = server.members
	for member in serverMembers:
		print("\t" + str(member) + " - set as 'Unverified'")
		await client.add_roles(member, role)


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='!verify for help'))
    print('Logged in as ' + client.user.name)

#TODO: overwrite discord.on_member_join
@client.command(name='verify',
		description='checks to see if a user is a valid UMBC student',
		breif='Verify yourself to allow access to this discord server',
		aliases=['v','verifyme','verifyMe','VerifyMe','Verify'],
		pass_context=True)
async def verify(*args):
	#await client.say(args[0].message.content) #debugging line
	message = args[0].message.content

	#!v, !v help
	if ' ' not in message or 'help' in message:
		await client.say('Welcome to the UMBC Overwatch Club Discord! To ensure the integrity of the club and access to this discord server we require all of our members to verify themselves with their emails. To verify your email use one of the following commands:'
		+ '\n\t!verify <Your UMBC Campus ID>'
		+ '\n\t!verify <Your UMBC UserID>' 
		+ '\n\t!verify <Your @umbc.edu Email>'
		+ '\n\nIf you are not a UMBC student or have any issues use the following command for an OWC admin to PM you with further instructions.')
	#!v <umbc argument>
	else:
		await client.say('verifying ID... please hold') #debugging line
		res = authenticate.authenticateUser(message)

		# Check result
		if(res == 0):
			print("Check failed.")
			await client.say('Sorry, either we could not verify your ID or something else unexpected went wrong. Please try again.\nverify_simple_search_check_error')
		elif(res == 1):
			print("Check succeeded.")
			await client.say("Your UMBC status has been verified, welcome to the UMBC Overwatch Club")
		elif(res == 2):
			print("Further contact needed.")
			await clinet.say("Sorry, but we are unable to verify certain emails, you will be contacted by a server admin to complete your verification")
			


''' Run '''
if __name__ == '__main__':
	token = fetchToken()
	client.loop.create_task(list_servers())
	if(token == 0):
		print("Token was not found, therefore bot can't run.")
		exit()
	else:
		client.run(token)
