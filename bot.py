# bot.py
import os
import json
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import numpy as np
import smtplib

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

# customizable
auth_channel = 'auth'
auth_role    = 'COSC 102'
email_tag    = '@vols.utk.edu'

# retrieve bot email credentials used for user authentication
async def get_credentials():
    return os.getenv('BOT_EMAIL_USER'), os.getenv('BOT_EMAIL_PASS')

# send authentication email to unauthenticated users
async def send_auth_email(user, passkey):
    BOT_EMAIL, BOT_PASS = await get_credentials()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(BOT_EMAIL, BOT_PASS)
    msg = f"Hello {user},\n\nCopy and paste the following code into the #auth channel: {passkey}\n\n-Sincerely, UTK Auth Bot"
    s.sendmail(BOT_EMAIL, str(user)+email_tag, msg)
    s.quit()

# check if a key already exists
def key_exists(user):
    data = {} # json dict placeholder
    if os.path.getsize('members.json') != 0: # if members.json is not empty...
        with open('members.json') as f:      
            data = json.load(f)              # read dict into data

    with open('members.json', 'w') as f:     
        if str(user) in data:
            json.dump(data, f, indent=2)
            f.close()
            return True
    return False

# updates member list for auth tracking
def update_members(auth_pair):
    data = {} # json dict placeholder
    if os.path.getsize('members.json') != 0: # if members.json is not empty...
        with open('members.json') as f:      
            data = json.load(f)              # read dict into data

    with open('members.json', 'w') as f:     
        data[auth_pair[0]] = auth_pair[1]
        print(data)
        json.dump(data, f, indent=2)

def remove_member(user):
    data = {}
    if os.path.getsize('members.json') != 0:
        with open('members.json') as f:
            data = json.load(f)
    with open('members.json', 'w') as f:
        data.pop(str(user), None)
        json.dump(data, f, indent=2)

# return passkey mapped to user ID from members.json
async def get_auth_pair(user):
    f = open('members.json')
    print(f'data[{str(user)}]')
    data = json.load(f)
    f.close()
    print(data)
    if str(user) in data:
        return data[str(user)]
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
    print(f'{bot.user} is online!')

# user authentication via Discord command !auth [netid]
@bot.command(name='auth')
async def auth(ctx: commands.Context, *, netid=None):
    member = ctx.message.author
    if is_auth(member):
        return
    if netid is None:
        await ctx.send(f"{member.mention} Please enter a valid UTK NetID!")
        return
    if key_exists(member.id):
        await ctx.send(f'{member.mention} there already exists a passcode for this NetID. Type `!reset` to reset your passcode.')
        return
    
    passkey = ''.join([str(number) for number in np.random.randint(10, size=6)]) # generate passkey
    auth_pair = (member.id, passkey)                                             # serialize ID & key
    update_members(auth_pair)
    await send_auth_email(netid, passkey)                                       # send auth email
    response = f"{member.mention} Check your UTK email and enter the code received into the chat."
    await ctx.send(response)


# read passkey for valid match
@bot.command(name='verify')
async def verify(ctx: commands.Context, *, passkey: str):
    member = ctx.message.author
    if is_auth(member):
        return

    # if passkey matches members.json, assign Student role and confirm authentication
    if passkey == await get_auth_pair(member.id):
        await ctx.message.channel.send(f"{member.mention} Authentication succesful!")
        await assign_role(member)
        remove_member(member.id)
    return

# resets passkey if it already exists in members.json
@bot.command(name='reset')
async def reset(ctx: commands.Context):
    if is_auth(ctx.message.author):
        await ctx.send(f'{ctx.message.author.mention} you\'re already authorized!')
        return
    remove_member(ctx.message.author.id)
    await ctx.send(f'{ctx.message.author.mention} your passcode has been reset!')
    return

bot.run(TOKEN)
