# UMBCOW-Auth

Discord authentication for the UMBC Overwatch server. Matches student e-mail with a valid student e-mail. Otherwise, allows a current server member to allow access to a guest or a visitor from another university to register themselves as a representative.

## Getting Started

The code is made specifically for the UMBC Overwatch server however if someone wants to run it elsewhere, the following are steps to get the bot up and running.

### Prerequisites

The bot runs off of Python 3.7.3 currently, using the [discord.py library](https://discordpy.readthedocs.io/en/latest/). No other libraries are required. The bot has not been tested on any other versions of Python.

### Installing

First, clone the repository and navigate to the clone. Then, create the following files
```
tokens.json reps.json verified.json visitors.json
```
These will be used for keeping track of validated users and storing other important information used by the bot.
Inside of the `tokens.json` file, add the following entries
```
{
  "bot_token" : "BOT TOKEN GOES HERE",
  "command_prefix" : "CHOSEN PREFIX FOR BOT COMMANDS GOES HERE",
  "server_id" : "ID OF THE DESIGNATED DEPLOYMENT SERVER GOES HERE"
}
```
Now the bot is able to run using `python bot.py`!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
