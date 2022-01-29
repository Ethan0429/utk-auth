# bot.py
import os
import json
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import numpy as np
import smtplib
from canvasapi import Canvas

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')
# Canvas API URL
API_URL = 'https://utk.instructure.com/'
# Canvas API key
API_KEY = os.getenv('CANVAS_KEY')
canvas = Canvas(API_URL, API_KEY)
CONST_COSC102_COURSE_ID = 139798
users = {}
# customizable
auth_channel = 'auth'
auth_role    = 'COSC 102'
email_tag    = '@vols.utk.edu'
# retrieve bot email credentials used for user authentication
async def get_credentials():
    return os.getenv('BOT_EMAIL_USER'), os.getenv('BOT_EMAIL_PASS')

def catch_invalid_login_id(user):
    try:
        return str(user.login_id)
    except AttributeError:
        pass

def catch_invalid_login_name(user):
    try:
        return str(user.name)
    except AttributeError:
        pass

def get_student_names():
    course = canvas.get_course(CONST_COSC102_COURSE_ID)
    users = {catch_invalid_login_id(user): catch_invalid_login_name(user) for user in course.get_users()} 
    return users
# send authentication email to unauthenticated users
async def send_auth_email(user, passkey):
    BOT_EMAIL, BOT_PASS = await get_credentials()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(BOT_EMAIL, BOT_PASS)
    msg = f'Hello {user},\n\nCopy and paste the following code into the #auth channel: {passkey}\n\n-Sincerely, UTK Auth Bot'
    s.sendmail(BOT_EMAIL, user+email_tag, msg)
    s.quit()

# check if a key already exists
def key_exists(user):
    data = {} # json dict placeholder
    try: # if members.json is not empty...
        with open('members.json', 'r') as f:      
            data = json.load(f)              # read dict into data
    except json.JSONDecodeError:
        return False
    
    if user in data:
        return True
    return False

# updates member list for auth tracking
def update_members(auth_id):
    data = { 
        auth_id[0]: 
        { 
            'passkey': auth_id[1],
            'netid': auth_id[2]
        }
    }
    try: # if members.json is not empty...
        with open('members.json') as f:      
            new_data = json.load(f) # read dict into data
            data = new_data
    except json.JSONDecodeError as e:
        print(e)
        pass
    with open('members.json', 'w') as f:
        data[auth_id[0]] = { 
            'passkey': auth_id[1],
            'netid': auth_id[2] 
        }
        
        print(data)
        json.dump(data, f, indent=2)

def remove_member(user):
    data = {}
    try:
        with open('members.json') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pass

    with open('members.json', 'w') as f:
        data.pop(user, None)
        json.dump(data, f, indent=2)

# return passkey mapped to user ID from members.json
async def get_auth_id(user):
    f = open('members.json', 'r')
    print(f'data[{user}]')
    data = json.load(f)
    f.close()
    print(data)
    if user in data:
        return data[user]
    return None

# check is user is already authenticated (has Student role)
def is_auth(user):
    print('checking authorization')
    roles = [str(role) for role in user.roles]
    if auth_role in roles:
        print(f'{user} is already authenticated!')
        return True
    return False

# add auth role to user
async def assign_role(user):
    if is_auth(user):
        return
    role = get(user.guild.roles, name=auth_role)
    await user.add_roles(role)

@bot.event
async def on_ready():
    global users
    users = get_student_names()
    print(f'{bot.user} is online!')
    

# user authentication via Discord command !auth [netid]
@bot.command(name='auth')
async def auth(ctx: commands.Context, *, netid=None):
    member = ctx.message.author
    str_member_id = str(member.id)
    if is_auth(member):
        return
    if netid is None:
        await ctx.send(f'{member.mention} Please enter a valid UTK NetID!')
        return
    if key_exists(str_member_id):
        await ctx.send(f'{member.mention} there already exists a passcode for this NetID. Type `!reset` to reset your passcode.')
        return
    
    passkey = ''.join([str(number) for number in np.random.randint(10, size=6)]) # generate passkey
    auth_id = (str_member_id, passkey, netid)                                             # serialize ID & key
    update_members(auth_id)
    #await send_auth_email(netid, passkey)                                        # send auth email
    response = f'{member.mention} Check your UTK email and enter the code received into the chat.'
    await ctx.send(response)


# read passkey for valid match
@bot.command(name='verify')
async def verify(ctx: commands.Context, *, passkey: str):
    member = ctx.message.author
    str_member_id = str(member.id)
    if is_auth(member):
        return

    auth_id = await get_auth_id(str_member_id)

    # if passkey matches members.json, assign Student role and confirm authentication
    if passkey == auth_id['passkey']:
        await ctx.message.channel.send(f'{member.mention} Authentication succesful!')
        await assign_role(member)
        await member.edit(nick=users[auth_id['netid']])
        remove_member(str_member_id)
    return

# resets passkey if it already exists in members.json
@bot.command(name='reset')
async def reset(ctx: commands.Context):
    member = ctx.message.author
    str_member_id = str(member.id)
    if is_auth(member):
        await ctx.send(f'{member.mention} you\'re already authorized!')
        return
    remove_member(str_member_id)
    await ctx.send(f'{member.mention} your passcode has been reset!')
    return

bot.run(TOKEN)
