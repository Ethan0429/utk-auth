# Description

Discord bot that authenticates UTK students via email verification & integrates username enforcement on a per-server basis via Canvas name registry.

# Usage

The bot has 3 commands, all of which are only effective if the user does not have an auth role already. _Note: none of these command arguments include brackets_
- `/auth [NetID]`: takes a single argument which is your UTK NetID.
- `/verify [6-digit passcode]`: takes a single argument which is the passcode received in your UTK email from `/auth`
- `/reset`: resets your authentication status if you've mistyped your NetID.

### Authentication

As a new user to a UTK server, simply type and enter:

`/auth [netid]` (without the brackets)

For example:

```
/auth bricker1
```

If nothing goes wrong, an email should be sent to the UTK email (@vols.utk.edu) pertaining to your NetID. **Note that this email is likely located in `spam` or `quarantined` folder for Gmail/Outlook respectively.**

### Verification

Within the email should be a verification code. Simply type and enter the verification code to verify with the bot:

`/verify [code] (without the brackets)`

For example:

```
/verify 12345
```

If nothing goes wrong, the user should be authenticated and granted access to its role's channels and privileges, along with their server nickname being changed to reflect their student identity.

### Reset

If any problems are encountered along the way, the user can reset the authentication process.

```
/reset
```

This removes any existing records for the Discord user, allowing them to repeat the authentication process.

# Development

## Structure

The project is structured relatively neatly so that each module has its own job(s).

- `bot_vars.py` handles variables that are used throughout the bot.
- `bot.py` handles all the front-facing bot logic and some implementation.
- `canvas_utils.py` handles special Canvas-API-related functions that are used in the bot code.
- `utk_mail.py` handles the authentication email service.
- `bot_utils.py` contains helper functions to be used in `bot.py`.

## Setup

```python3
DISCORD_TOKEN   = os.getenv('DISCORD_TOKEN') # Discord app key for interfacing with their API
CANVAS_API_KEY  = os.getenv('CANVAS_KEY')    # Canvas app key for interfacing with their API
CONST_COURSE_ID = os.getnenv(COURSE_ID)      # Canvas course ID for any particular course. Used to reference student names
```

- `DISCORD_TOKEN` refers to the Discord bot's generated token, which should be unchanging. No config necessary.
- `CANVAS_API_KEY` refers to the Canvas generated API Key. The API key must have access to the student list for a Canvas course in order for the bot to function, otherwise no users will be returned. The API key is handled through the [Railway](https://railway.app) deployment's environment variables. The API key should belong to either a TA or course instructor. You can learn how to generate an API key [here](https://community.canvaslms.com/t5/Student-Guide/How-do-I-manage-API-access-tokens-as-a-student/ta-p/273).
- `COURSE_ID` refers to the course ID specific to the Canvas course. This likely changes every semester and can be found in the Canvas course page's URL. (e.g. `https://utk.instructure.com/courses/190229/`, where `190229` is the ID) This is handled through the Railways deployment's environment variables.

and

```python3
async def get_credentials():
    return os.getenv('BOT_EMAIL_USER'), os.getenv('BOT_EMAIL_PASS') # the bot email/password
```
- `BOT_EMAIL_USER` refers to the email handle for a particular Gmail account.
- `BOT_EMAIL_PASS` refers to the app-generated password for that Gmail account. You can learn how to generate a Gmail app password [here](https://support.google.com/accounts/answer/185833?hl=en).

## Branches

The repo is currently split into 2 branches

1. `main`
2. `cosc101`

The branches *should* be identical aside from a few constants in `bot_vars.py`. In order for deployments to propogate for 102/101, changes must be pushed to their respective branches. The Discord bots for each of them are separate as well.

## Requirements

All requirements are listed in `requirements.txt`, and should only be worried about for local development. Otherwise Railway handles the environment.

If you are developing/testing locally, then I recommend using using `venv`.

```bash
python -m venv venv \
source ./venv/bin/activate \
./venv/bin/pip3 install -r requirements.txt
```

The above commands will setup the python environment in the cloned repo and install all dependencies in a localized python environment.

