# Description
Discord bot that authenticates UTK students via email verification

# Setup
Other than normal Discord-bot-integration, you must have your own `members.json` file and have your environment variables set accordingly in an `.env` file.
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

# Requirements
- Python 3.8 (possibly lower, but it was built with 3.8)
- discord.py
- python-dotenv
- numpy (necessary for the implementation but can easily be replaced with stock Python)
