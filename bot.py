import re, json, discord, asyncio, requests
from discord.ext import commands

# Init bot vars on startup
TOKEN = ""
COMMAND_PREFIX = ""
SERVER_ID = ""
with open("tokens.json") as f: 
    js = json.load(f)
    TOKEN = js['bot_token']
    COMMAND_PREFIX = js['command_prefix']
    SERVER_ID = js['server_id']


# Verification stuff
STUDENTS_JSON = "verified.json"
VISITOR_JSON = "visitors.json"
REPS_JSON = "reps.json"
UMBC_DIRECTORY_URL = "https://www.umbc.edu/search/directory/?search="

def id_in_use(discord_name, campus_id):

    with open(STUDENTS_JSON) as students:
        students = json.load(students)
        if campus_id in students.values() or discord_name in students.keys():
            return True
    return False

# Bot class handler
class UMBCBot(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_reaction_remove(self, reaction, user):

        server = self.get_guild(int(SERVER_ID))
        
        # Get the user as a member of the server
        try:
            member = server.get_member_named(user.name)
        except:
            await user.send("It doesn't appear you're a member of our UMBC Overwatch server!")
            return
        await self.new_member(member)

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        
        # Verify
        if "!v" in message.content:
            print('\tVerifying user')
            msg_split = message.content.split(" ")
            if len(msg_split) != 2 or len(msg_split[0]) != 2:
                print("\tInvalid format")
                try:
                    await message.author.send("Looks like you used the wrong format, please try again with '!v <UMBC ID>'!")
                except:
                    print("Weird messaging error")
            else:
                server = self.get_guild(int(SERVER_ID))
                
                # Get the user as a member of the server
                try:
                    member = server.get_member_named(str(message.author))
                except:
                    await message.author.send("It doesn't appear you're a member of our UMBC Overwatch server!")
                    return
                await self.verify(member, msg_split[1])
                
        elif "!resume" in message.content:
            print("Resuming verification for %s" % (str(message.author)))
            # Get the user as a member of the server
            try:
                member = server.get_member_named(message.author)
            except:
                await message.author.send("It doesn't appear you're a member of our UMBC Overwatch server!")
                return
            await self.new_member(member)

        # Links
        elif "!links" in message.content:
            print("\tSending links")
            await message.author.send("Website: https://my3.my.umbc.edu/groups/overwatch\n"
                                    + "Twitch: https://www.twitch.tv/umbc_overwatch\n"
                                    + "Twitter: https://twitter.com/UMBCOverwatch/\n"
                                    + "Instagram: https://www.instagram.com/umbcoverwatch/\n"
                                    + "Overbark Twitter: https://twitter.com/UMBC_Overbark\n"
                                    + "Overbark Twitch: https://www.twitch.tv/umbcesports\n")

        # Help
        elif "!help" in message.content:
            print("\tSending help")
            await message.author.send("Here's my available commands:\n"
                                    + "`!v UMBC-ID\nAllows the user to verify themself on the server using their UMBC ID`\n"
                                    + "`!links\nSends the user all the Overwatch club's social media links`\n"
                                    + "`!undo\nRemoves the user's name from all registry entries`\n"
                                    + "`!help\nSends you this list`\n")

        # Undo Entry
        elif "!undo" in message.content:
            print("\tPerforming undo")
            # Check for the user's name in each of the registries
            try:
                for cur_json_fn in [STUDENTS_JSON, VISITOR_JSON, REPS_JSON]:
                    with open(cur_json_fn) as cur_json:
                        cur_data = json.load(cur_json)
                    if cur_data == None:
                        raise IOError
                    if str(message.author) in cur_data.keys():
                        print("\tFound user '" + str(message.author) + "' in " + cur_json_fn)
                        # Delete entry
                        cur_data.pop(str(message.author), None)
                        with open(cur_json_fn, 'w') as cur_json:
                            json.dump(cur_data, cur_json, indent=4)
                        await message.author.send("Your verification was successfully removed!")
                        return
            except IOError:
                print("\tIssue opening a JSON")
                await message.author.send("Sorry, the bot encountered an error. Please report this to an officer!")
                return
            # Reaches here if the name wasn't in any registries
            await message.author.send("Sorry, we couldn't find your name in any of the registries. If this is an issue, contact and officer!")

    async def validate_visitor(self, member, campus_id):

        print("Verifying that " + campus_id + " is a valid, registered ID...")
        stdnt_json = None

        # Get info from the student JSON
        try:
            with open (STUDENTS_JSON) as stdnt_f:
                stdnt_json = json.load(stdnt_f)
            if stdnt_json == None:
                raise IOError
        except IOError:
            print("Didn't receive a student JSON back - validate_visitor")
            return
        
        # Check invalid ID
        if campus_id not in stdnt_json.values():
            await member.send("Looks like your host isn't verified on this server, tell them to message me '!v CAMPUS_ID'!")
            return
        
        # Update Roles
        server = self.get_guild(int(SERVER_ID))
        server_roles = server.roles
        unver_role = None
        visitor_role = None
        for r in server_roles:
            if r.name == "Unverified":
                unver_role = r
            elif r.name == "Visitor":
                visitor_role = r
        if unver_role == None or visitor_role == None:
            return
        await member.remove_roles(unver_role)
        await member.add_roles(visitor_role)

        # Update JSON
        with open (VISITOR_JSON) as visitor_json:
            data = json.load(visitor_json)
        data.update({str(member) : campus_id})
        with open (VISITOR_JSON, 'w') as visitor_json:
            json.dump(data, visitor_json, indent=4)
        print("Added visitor entry for " + str(member))
        
        # Send user a message
        await member.send("You're now checked in as a visitor, enjoy!")

    async def verify(self, member, campus_id):
        
        print("Verifying\nDiscord User: " + str(member) + "\nCampus ID: " + campus_id)
        
        # Check if the campus id is already registered or the discord user is already in the database
        if id_in_use(str(member), campus_id):
            await member.send("Sorry partner, that ID is already registered. Please contact an officer if this is an error.")
            return

        # Try to verify the user using the UMBC directory
        url = UMBC_DIRECTORY_URL + campus_id
        r = requests.get(url)
        # Validate search request
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print("Request failed - couldn't reach UMBC website?")
            await member.send("Sorry! Looks like they cut off my internet so I can't reach the UMBC website. Please talk to an officer about this!")

        # Check that search found a result
        if (any(char.isdigit() for char in campus_id) and
            ('1 result found' in r.text)):
            await member.send("Found you! You'll receive your UMBC Student role in a moment. If it doesn't happen, contact an officer.")
            
            # Give role
            server = self.get_guild(int(SERVER_ID))
            server_roles = server.roles
            ver_role = None
            unver_role = None
            for r in server_roles:
                if r.name == "Verified":
                    ver_role = r
                elif r.name == "Unverified":
                    unver_role = r
            if ver_role == None or unver_role == None:
                return
            await member.add_roles(ver_role)
            await member.remove_roles(unver_role)
            await member.send("Your role has been assigned! Enjoy the server, and please read the #welcome-and-rules channel!")
            
            # Write the user to the students JSON
            with open (STUDENTS_JSON) as stdnt_json:
                data = json.load(stdnt_json)
            data.update({str(member) : campus_id})
            with open (STUDENTS_JSON, 'w') as stdnt_json:
                json.dump(data, stdnt_json, indent=4)
            print("Added student entry for " + str(member))
            
        else:
            await member.send("I couldn't find your ID in the directory. Feel free to try again later using !verify <campus id>, or contact and officer.")

    async def on_member_join(self, member):
        
        await self.new_member(member)

    async def new_member(self, member):
        # Give user the unverified role
        server = self.get_guild(int(SERVER_ID))
        server_roles = server.roles
        unver_role = None
        for r in server_roles:
            if r.name == "Unverified":
                unver_role = r
        if unver_role == None:
            self.close()
        await member.add_roles(unver_role)
        
        # Sends initial message to new member
        msg = await member.send('Welcome to the UMBC Overwatch server!\n' +
                          'Please react with one of the following emojis for a role!\n\n' +
                          '🐾 UMBC Student\n🚗 non-UMBC eSports Representative\n👥 Visitor')
        await msg.add_reaction("🐾")
        await msg.add_reaction ("🚗")
        await msg.add_reaction("👥")
        
        # Checks for a valid reaction response
        def check(reaction, user):
            print(reaction.emoji == '🐾')
            print(reaction.emoji == '🚗')
            return user == member and (reaction.emoji == "🐾" or reaction.emoji == "🚗" or reaction.emoji == "👥")

        # Checks for a valid campus ID response
        def check_msg(msg):
            return len(msg.content) == 7  # Expecting size of campus ID

        # Checks for a valid .edu e-mail
        def check_email(msg):
            return (re.search(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.+-]+\.edu$", msg.content) != None)

        # Checks for a valid college tag
        def check_tag(msg):
            return len(msg.content) > 0 and len(msg.content) < 5

        # Try and receive a reaction
        try:
            reaction, user = await self.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            print("Member join timed out for " + str(member))
            await member.send("Looks like you're busy, so whenever you want to continue your verification message me !resume and we can try again!")
            return
        else:
            # Handle UMBC students
            if reaction.emoji == "🐾":
                print(str(member) + " selected UMBC student")
                await member.send("bork bork, go retrievers!\nTo validate that you're a UMBC student, please send me a message with your UMBC campus ID! (ex: AB12345)")
                try:
                    message = await self.wait_for('message', timeout=30.0, check=check_msg)
                except asyncio.TimeoutError:
                    print("Member reaction timed out for " + str(member))
                    return
                await member.send("Received your ID! Validating...")
                await self.verify(member, message.content)
            # Handle non-UMBC students
            elif reaction.emoji == "🚗":
                print(str(member) + " selected non-UMBC student")
                # Get role objects
                server_roles = server.roles
                rep_role = None
                for r in server_roles:
                    if r.name == "University E-Rep":
                        rep_role = r
                if rep_role == None:
                    return
                # Ask the user for a valid .edu e-mail
                await member.send("Please send me your .edu e-mail address from your school for validation!")
                try:
                    edu_email = await self.wait_for('message', timeout=30.0, check=check_email)
                except asyncio.TimeoutError:
                    print("e-sports Rep e-mail request timed out")
                    return
                # Give role and then ask for tag
                await member.add_roles(rep_role)
                await member.remove_roles(unver_role)
                await member.send("Your e-mail looks good! Please send me a 1 to 4 character long tag for your college (ex: UMBC, UMD, TWSN)")
                try:
                    edu_tag = await self.wait_for('message', timeout=30.0, check=check_tag)
                except asyncio.TimeoutError:
                    print("e-sports Rep tag request timed out")
                # Set new nickname
                new_nick = "[" + edu_tag.content + "] " + member.name
                await member.edit(nick=new_nick)
                await member.send("*True Grit welcomes  you with open arms*\nWelcome to our server!")
                # Write to JSON
                with open (REPS_JSON) as reps_js:
                    data = json.load(reps_js)
                data.update({str(member) : str(edu_email.content)})
                with open (REPS_JSON, 'w') as reps_js:
                    json.dump(data, reps_js, indent=4)
                print("Added representative entry for " + str(member))
            # Handle visitors
            elif reaction.emoji == "👥":
                print(str(member) + " selected visitor role")
                await member.send("More friends! Please send me your UMBC host's campus ID! (ex: AB12345)")
                try:
                    message = await self.wait_for('message', timeout=30.0, check=check_msg)
                except asyncio.TimeoutError:
                    print("Timed out waiting for user id for visitor " + str(member))
                    return
                await self.validate_visitor(member, message.content)
def main():
    try:
        client = UMBCBot()
        client.run(TOKEN)
    except:
        main()

if __name__ == "__main__":
    main()