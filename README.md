# Description
Discord bot that authenticates UTK students via email verification & integrates username enforcement on a per-server basis via Canvas name registry.

# Bot Link
[Click here to add this bot to your server!](https://discord.com/api/oauth2/authorize?client_id=936087804033781801&permissions=8&scope=bot)

# Usage
The bot has 3 commands, all of which are only effective if the user does not have an auth role already. _Note: none of these command arguments include brackets_
- `!auth [NetID]`: takes a single argument which is your UTK NetID.
- `!verify [6-digit passcode]`: takes a single argument which is the passcode received in your UTK email from `!auth`
- `!reset`: resets your authentication status if you've mistyped your NetID.

As a new user to a UTK server, simply type and enter:

`!auth [netid]` (without the brackets)

If you've entered the command correctly and with a valid NetID, then you will receive an email from the bot containing a 6-digit passcode. All you have to do from there is copy/paste `!verify [passcode]` into the `#auth` channel. If done correctly, you will be assigned an auth role (`Student` by default) and will be allowed access to the server and its privileges. Good luck!

# Development
## Setup
Ignore from here on out if you don't plan on messing with the src at all.

[Other than normal Discord-bot-integration](https://discord.com/api/oauth2/authorize?client_id=936087804033781801&permissions=8&scope=bot), you must have your own `members.json` file and have your environment variables set accordingly in an `.env` file.
The following variables are subject to the individual's preferences:
```python3
TOKEN           = os.getenv('DISCORD_TOKEN')        # Discord app key for interfacing with their API
bot             = commands.Bot(command_prefix='!')  # Command prefix (!auth, ?auth, etc)
API_URL         = 'https://utk.instructure.com/'    # API url for Canvas. Depends on your institutions base Canvas url
API_KEY         = os.getenv('CANVAS_KEY')           # Canvas app key for interfacing with their API
CONST_COURSE_ID = 139798                            # Canvas course ID for any particular course. Used to reference student names
auth_channel    = 'auth'                            # Name of the Discord channel where authentication takes place
auth_role       = 'COSC 102'                        # Name of authenticated Discord role
email_tag       = '@vols.utk.edu'                   # Email domain for your particular institution
```
and
```python3
async def get_credentials():
    return os.getenv('BOT_EMAIL_USER'), os.getenv('BOT_EMAIL_PASS') # the bot email/password
```

## Requirements
- Python 3.8 (possibly lower, but it was built with 3.8)
- discord.py
- python-dotenv (or tweak the code for native env variables)
- numpy (necessary for the implementation but can easily be replaced with stock Python)
- canvasapi
- smtplib (my personal choice of automated emailing)
