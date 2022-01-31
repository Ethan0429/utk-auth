import os, sys
from canvasapi import Canvas
from dotenv import load_dotenv
from collections import namedtuple

if os.path.exists('.env'):
    pass
else:
    with open('.env') as f:
        f.writelines([
            '# .env',
            'DISCORD_TOKEN=',
            'BOT_EMAIL_USER='
            'BOT_EMAIL_PASS=',
            'CANVAS_KEY='
        ])
    print('.env file generated! Exiting bot script.\nFill the appropriate fields in the .env file before running the script again!')
    sys.exit()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
auth_channel = 'auth'
auth_role    = 'COSC 102'
email_tag    = '@vols.utk.edu'

# Canvas API URL
API_URL = 'https://utk.instructure.com/'
# Canvas API key
API_KEY = os.getenv('CANVAS_KEY')
canvas = Canvas(API_URL, API_KEY)
CONST_COSC102_COURSE_ID = 139798
users = {}

AuthID = namedtuple('AuthID', ['member_id', 'passkey', 'netid'])
