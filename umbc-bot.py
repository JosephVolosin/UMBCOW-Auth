# discord.py houses the code for the Discord bot that will run on the server.
# This file uses discord-keys.txt which houses the Discord API keys, this file
#   is hidden for security.
import authenticate, discord, asyncio, aiohttp, whitelist, visitor
from discord.ext.commands import Bot
'''
Constants
'''
BOT_PREFIX = ('?', '!')
SERVER_ID = '360868374244491264'
client = Bot(command_prefix=BOT_PREFIX)
OFFICERS = ["JosephPV#1306", "octomaidly#0008", "JereDawg99#5649", "Maineo1#9403"]
IAMROLES = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "Support", "DPS", "Tank",
			"Flex", "Defense", "Seoul Dynasty", "Shanghai Dragons", "London Spitfire", "Houston Outlaws", "LA Valiant",
			"Dallas Fuel", "LA Gladiators", "NY Excelsior", "Florida Mayhem", "Boston Uprising", "SF Shock", "Philadelphia Fusion"]

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

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print('Current servers:')
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

# checkOfficer(username) checks to see if username is an officer.
def checkOfficer(username):

	if username in OFFICERS:
		return True
	return False	

''' Bot Methods '''
# setupServer() creates the unverified role 
@client.command(name='setupServer',
                description='sets the server up to use the verification system',
                breif='sets the server up to use the verification system',
                aliases=['setupserver', 'setup', 's'],
                pass_context=True)
async def setupServer(*args):
	if(checkOfficer(str(args[0].message.author))):
		# Create the 'Unverified' role
		try:
			server = args[0].message.author.server
		except AttributeError:
			await client.send_message(args[0].message.author, "You must run that command from a server.")
			return
		await client.create_role(server, name='Unverified')

		# Create the 'Verified' role
		await client.create_role(server, name="Verified")
	else:
		client.send_message(args[0].message.author, "You are not verified to use this command.")

# setAllNotVerified() gives everyone the unverified role
@client.command(name='setAllNotVerified',
		description='setsall users in the server to a NotVerified role',
		breif='sets all users in the server to a NotVerified role',
		aliases=['setANV','fukAllYall'],
		pass_context=True)
async def setAllNotVerified(*args):

	if(checkOfficer(str(args[0].message.author))):
		try:
			server = args[0].message.author.server
		except AttributeError:
			await client.send_message(args[0].message.author, "You must run that command from a server.")
			return
		role = discord.utils.get(server.roles, name='Unverified')
		serverMembers = server.members
		for member in serverMembers:
			print("\t" + str(member) + " - set as 'Unverified'")
			await client.add_roles(member, role)
	else:
		client.send_message(args[0].message.author, "You are not verified to use this command.")

# on_ready() is the bot's startup
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='!verify for help'))
    print('Logged in as ' + client.user.name)

# website() sends the user that called it a link to the website
@client.command(name="website",
				description = "Sends the user a link to the e-sports website.",
				aliases=['w'],
				pass_context=True)
async def website(*args):
	await client.send_message(args[0].message.author, 
					' http://umbcesports.com/overwatch/ for more info!')

# verify() verifies a user account with the umbc directory
@client.command(name='verify',
		description='checks to see if a user is a valid UMBC student',
		breif='Verify yourself to allow access to this discord server',
		aliases=['v','verifyme','verifyMe','VerifyMe','Verify'],
		pass_context=True)
async def verify(*args):
	author = args[0].message.author
	message = args[0].message.content
	if(("!v" in message) or ("!verify" in message)):
		#!v, !v help
		if ' ' not in message or 'help' in message:
			await client.say('Welcome to the UMBC Overwatch Club Discord! To ensure the integrity of the club and access to this discord server we require all of our members to verify themselves with their emails. To verify your email use one of the following commands:'
			+ '\n\t!verify <Your UMBC Campus ID>'
			+ '\n\t!verify <Your UMBC UserID>' 
			+ '\n\t!verify <Your @umbc.edu Email>'
			+ '\n\nIf you are not a UMBC student or have any issues use the following command for an OWC admin to PM you with further instructions.')
		#!v <umbc argument>
		else:
			await client.send_message(author, 'verifying ID... please hold') #debugging line
			# Check whitelist
			res = authenticate.checkExistingAuth(str(author), message)
			if(res == 0):
				# Log to terminal TODO - create log file?
				print("\t" + str(author) + ": sent an already used token.")
				print("\t\t" + message)
				await client.send_message(author, "Sorry, your e-mail/ID has already been used to authenticate an account. Please contact an officer if this is wrong.")
			elif(res == 2):
				print("\t" + str(author) + ": attempted to authenticate an authenticated account.")
				await client.send_message(author, "It appears your current discord account is already authenticated.. If you are missing the role, please contact an officer.")
			else:
				# Send request
				res = authenticate.authenticateUser(message)
				server = client.get_server(SERVER_ID)
				verified = discord.utils.get(server.roles, name='Verified')
				unverified = discord.utils.get(server.roles, name='Unverified')
				# Check result
				if(res == 0):
					print("Check failed.")
					await client.send_message(author, 'Sorry, either we could not verify your ID or something else unexpected went wrong. Please try again.\nverify_simple_search_check_error')
				elif(res == 1):
					print("Check succeeded.")
					await client.send_message(author, "Your UMBC status has been verified, welcome to the UMBC Overwatch Club")
					member = None
					for mem in server.members:
						if(mem == author):
							member = mem
					if(member == None):
						print("The user is not a member of the server.")
						return 0
					await client.add_roles(member, verified)
					await client.remove_roles(member, unverified)
					message = message[message.find(" ") + 1:]
					whitelist.write(str(author) + "," + message)
				elif(res == 2):
					print("Further contact needed.")
					await client.send_message(author, "Sorry, but we are unable to verify certain emails, you will be contacted by a server admin to complete your verification")


# on_member_join() messages a new user and tells them how to verify, all of 
# verify will then be carried out in PM's
@client.event
async def on_member_join(*args):
	
	# Send user a PM greeting them and telling them to verify and sets user as unverified
	server = client.get_server(SERVER_ID)
	unverified = discord.utils.get(server.roles, name='Unverified')
	print("Sending new user a message: " + str(args[0]))
	print(type(args[0]))
	await client.add_roles(args[0], unverified)
	await client.send_message(args[0], "Welcome to the UMBC Overwatch server! We " +
									"require users to authenticate their " +
									"Discord accounts by using their campus ID " +
									"or thseir username (ex: USERNAME@umbc.edu)" +
									". Please send me a message in the format:" +
									"\n`!v <CampusID>`\nor\n`!v <Username>`")
	print("Message sent.")

# on_message() will check the bot's PMs for command messages.
@client.event
async def on_message(*args):
	message = args[0].content
	server = client.get_server(SERVER_ID)
	visitor_role	= discord.utils.get(server.roles, name='Visitor')
	unverified_role	= discord.utils.get(server.roles, name='Unverified')
	# Check visitors for cleanup
	usrs_remove = visitor.removeOldVisitors()
	for usr in usrs_remove:
		member = server.get_member_named(usr)
		await client.remove_roles(member, visitor_role)
		await client.add_roles(member, unverified_role)
	await client.process_commands(args[0])

@client.command(name="stop",
				description="DEBUGGING: kills bot.",
				pass_context=True)
async def stop(*args):
	print("Attempting to stop client..")
	if(checkOfficer(str(args[0].message.author))):
		await client.logout()
		print("Ending client..")
	else:
		await client.send_message(args[0].message.author, "Nice try, but only officers can run that command.")
		print(str(args[0].message.author) + " attempted to shutdown the bot.")

# Message should be in the form of !visitor <discord-tag>
@client.command(name="visitor",
				description="Check-in a visitor to the server.",
				pass_context=True)
async def visitor_add(*args):

	print("Checking in a visitor..")
	# Check that the person calling this is a verified member
	server = client.get_server(SERVER_ID)
	verified_role = discord.utils.get(server.roles, name='Verified')
	member = args[0].message.author
	print(type(member))
	if(verified_role not in member.roles):
		print("\t" + str(member) + " tried to add a visitor without being verified.")
		await client.send_message(member, "You are not allowed to add visitors if you yourself, are a visitor.")
		return 0
	# Check that there was a valid member passed to the bot
	msg_split = args[0].message.content.split(" ")
	if(len(msg_split) == 1):
		print("\tVisitor called without any argument.")
		await client.send_message(member, "Proper use of this command is '!visitor <discord-tag>'")
		return 0
	visitor_tag = msg_split[1]
	visitor_mem = None
	# Check that this member is a member of the server
	for mem in server.members:
		if(str(mem) == visitor_tag):
			visitor_mem = mem
	# Check that the user was found on the server
	if(visitor_mem == None):
		print("\t" + visitor_tag + " was not found on the server.")
		await client.send_message(member, "Your visitor was not found on this server. Please make sure they've joined.")
		return 0
	# Give the visitor the visitor role, remove unverified, write to visitors
	visitor_role = discord.utils.get(server.roles, name='Visitor')
	unverified_role = discord.utils.get(server.roles, name='Unverified')
	await client.add_roles(visitor_mem, visitor_role)
	await client.remove_roles(visitor_mem, unverified_role)
	visitor.write(str(member) + "," + str(visitor_mem))
	print(str(member) + " gave visitor status to " + str(visitor_mem) + ".")

# Allows users to update their roles in Discord of Rank and Role automatically thru API
@client.command(name="update",
				description="Update Overwatch specific roles: rank and role.",
				pass_context=True)
async def update(*args):

	message = args[0].message
	member = message.author
	rank_roles = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"]
	role_roles = ["Support", "DPS", "Tank"]
	# Rank ranges are the tops of each bracket
	rank_ranges = { "Bronze" : 1500, "Silver" : 2000, "Gold" : 2500, "Platinum" : 3000, "Diamond" : 3500, "Master" : 4000 }
	# All possible characters, listed by their role, comma delimitted
	role_chars = { "Support" : "Lucio,Ana,Zenyatta,Moira,Mercy,Brigitte",
				   "DPS"	 : "Bastion,Doomfist,Genji,Hanzo,Junkrat,McCree,Mei,Pharah,Reaper,Soldier: 76,Sombra,Symettra,Torbjörn,Tracer,Widowmaker",
				   "Tank"	 : "D.Va,Orisa,Reinhardt,Roadhog,Winston,Wrecking Ball,Zarya" }
	
	print(str(member) + " is updating roles..")
	# Expected input is !update <BTAG>

# Lets users set roles that are designated in IAMROLES
@client.command(name="iam",
				description="Allow the user to set any of the determined roles by themselves.",
				pass_context=True)
async def iam(*args):

	message = args[0].message.content
	member = args[0].message.author
	server = client.get_server(SERVER_ID)
	message_split = message.split("!iam")
	# Check if there was no arguments
	print(message_split)
	if(len(message_split) == 1):
		print("\tiam called without any argument.")
		await client.send_message(member, "Proper use of this command is '!iam <role>. To see possible roles, use !iam help'")
		return 0
	# Help message
	if("help" in message):
		print("\tGiving !iam help message..")
		# Creates string of all roles so that bot only has to send one message.
		role_string = "\n"
		for r in IAMROLES:
			role_string += "\t" + r + "\n"
		await client.send_message(member, "Possible roles are as follows: " + role_string)
	# Attempt to give user the role
	else:
		role_usr_str = message_split[1]
		role_usr_obj = discord.utils.get(server.roles, name=role_usr_str)
		# Check that role is valid
		if(role_usr_str not in server.roles):
			await client.send_message(member, "That role does not exist, or you do not have access to it.")
			return 0
		# Check if user already has role
		if(role_usr_str in member.roles):
			await client.send_message(member, "You already have that role.")
			return 0
		# Give user the role
		new_role = discord.utils.get(server.roles, name=role_usr_str)
		print("Giving user " + str(member) + " the role: " + role_usr_str)
		await client.add_roles(member, new_role)
		await client.send_message(member, "Role added!")
	
''' Run '''
if __name__ == '__main__':
	token = fetchToken()
	client.loop.create_task(list_servers())
	if(token == 0):
		print("Token was not found, therefore bot can't run.")
		exit()
	else:
		client.run(token)
