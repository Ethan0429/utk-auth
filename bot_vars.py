import os
from canvasapi import Canvas
from collections import namedtuple

# Uncomment if using dotenv
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN_')

auth_channel = 'auth'
auth_role    = 'COSC 102'
email_tag    = '@vols.utk.edu'

# Canvas API URL
API_URL = 'https://utk.instructure.com/'
# Canvas API key
API_KEY = os.getenv('CANVAS_KEY')
canvas = Canvas(API_URL, API_KEY)
CONST_COSC102_GUILD_ID = 935991929978621962
CONST_COSC102_GRADER_ROLE_ID = 943277040445038612
CONST_COSC102_COURSE_ID = 154574
CONST_COSC102_GRADING_CHANNEL_ID = 1017518807654346853
users = {}

AuthID = namedtuple('AuthID', ['member_id', 'passkey', 'netid'])
