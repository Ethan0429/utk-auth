import os, sys
from canvasapi import Canvas
from dotenv import load_dotenv
from collections import namedtuple

# if using dotenv, un-comment:

# if os.path.exists('.env'):
#     pass
# else:
#     with open('.env', 'w') as f:
#         f.writelines([
#             '# .env\n',
#             'DISCORD_TOKEN=\n',
#             'BOT_EMAIL_USER=\n'
#             'BOT_EMAIL_PASS=\n',
#             'CANVAS_KEY=\n'
#         ])
#     print('.env file generated! Exiting bot script.\nFill the appropriate fields in the .env file before running the script again!')
#     sys.exit()

# load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

print(f"Discord bot token: {TOKEN}\n")

auth_channel = 'auth'
auth_role    = 'COSC 102'
email_tag    = '@vols.utk.edu'

# Canvas API URL
API_URL = 'https://utk.instructure.com/'
# Canvas API key
API_KEY = os.getenv('CANVAS_KEY')
canvas = Canvas(API_URL, API_KEY)
CONST_COSC102_COURSE_ID = 154574
users = {}

AuthID = namedtuple('AuthID', ['member_id', 'passkey', 'netid'])
