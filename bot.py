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
auth_role    = 'Student'
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

# updates member list for auth tracking
def update_members(data):
    with open('members.json', 'w') as fp:
        json.dump(data, fp, indent=2)


# return passkey mapped to user ID from members.json
async def get_auth_pair(user):
    f = open('members.json')
    data = json.load(f)
    for key, value in data.items():
        if str(key) == str(user):
            f.close()
            return str(value)
    f.close()
    return None

# check is user is already authenticated (has Student role)
def is_auth(user):
    if auth_role in user.roles:
        return True
    return False

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
    if is_auth(ctx.author):
        return
    if netid is None:
        response = f"{ctx.message.author.mention} Please enter a valid UTK NetID!"
        await ctx.send(response)
        return
    
    passkey = ''.join([str(number) for number in np.random.randint(10, size=6)]) # generate passkey
    auth_pair = {ctx.message.author.id: passkey}                                 # serialize ID & key
    update_members(auth_pair)
    await send_auth_email(netid, passkey)                                        # send auth email
    response = f"{ctx.message.author.mention} Check your UTK email and enter the code received into the chat."
    await ctx.send(response)


# read passkey for valid match
@bot.event
async def on_message(message):
    if (message.author.id == bot.user.id) or (str(message.channel) != auth_channel):
        return
    await bot.process_commands(message)
    if is_auth(message.author):
        return

    # if passkey matches members.json, assign Student role and confirm authentication
    if str(message.content) == await get_auth_pair(message.author.id):
        await message.channel.send(f"{message.author.mention} Authentication succesful!")
        await assign_role(message.author)
    return

bot.run(TOKEN)
