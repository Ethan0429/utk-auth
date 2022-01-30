# Description
Discord bot that authenticates UTK students via email verification

# Bot Link
[Click here to add this bot to your server!](https://discord.com/api/oauth2/authorize?client_id=936087804033781801&permissions=8&scope=bot)

# Usage
The bot has only one command `!auth` that takes a single argument which is your UTK NetID. You're only able to use the `!auth` command if you are both role-less **and** in the `#auth` channel. Otherwise it will not work. 

As a new user to a UTK server, simply type and enter:

`!auth [netid]` (without the brackets)

If you've entered the command correctly and with a valid NetID, then you will receive an email from the bot containing a 6-digit passcode. All you have to do from there is copy/paste the passcode into the `#auth` channel. If done correctly, you will be assigned an auth role (`Student` by default) and will be allowed access to the server and its privileges. Good luck!

# Development
## Setup
Ignore from here on out if you don't plan on messing with the src at all.

[Other than normal Discord-bot-integration](https://discord.com/api/oauth2/authorize?client_id=936087804033781801&permissions=8&scope=bot), you must have your own `members.json` file and have your environment variables set accordingly in an `.env` file.
The following variables are customizable:
```python3
bot = commands.Bot(command_prefix='!')

# customizable
auth_channel = 'auth'
auth_role    = 'Student'
email_tag    = '@vols.utk.edu'
```
and
```python3
async def get_credentials():
    return os.getenv('BOT_EMAIL_USER'), os.getenv('BOT_EMAIL_PASS')
```

## Requirements
- Python 3.8 (possibly lower, but it was built with 3.8)
- discord.py
- python-dotenv
- numpy (necessary for the implementation but can easily be replaced with stock Python)
