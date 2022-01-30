import os
from canvasapi import Canvas
from dotenv import load_dotenv
from collections import namedtuple

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
