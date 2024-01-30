import os
from canvasapi import Canvas
from collections import namedtuple

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

auth_channel = "auth"
EMAIL_TAG = "@vols.utk.edu"
AUTH_ROLE = os.getenv("AUTH_ROLE")
AUTH_ROLE_ID = os.getenv("AUTH_ROLE_ID")
GUILD_ID = os.getenv("GUILD_ID")
# TA_ROLE_ID = os.getenv("TA_ROLE_ID")
CANVAS_COURSE_URL_ID = os.getenv("CANVAS_COURSE_URL_ID")

AuthID = namedtuple("AuthID", ["member_id", "passkey", "netid"])

# stores dictionary of net ID's and users
users = {}

# Canvas API URL
API_URL = "https://utk.instructure.com/"

# Canvas API key
CANVAS_API_KEY = os.getenv("CANVAS_API_KEY")

# init Canvas object
canvas = Canvas(API_URL, CANVAS_API_KEY)
