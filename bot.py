# bot.py
import os
import json
from discord.ext import commands
from dotenv import load_dotenv
import numpy as np

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')
unauthenticated_user = ''
# accesses bot email credentials used for user authentication

def get_credentials():
    return os.getenv('BOT_EMAIL_USER'), os.getenv('BOT_EMAIL_PASS')

# updates member list for auth tracking

def update_members(data):
    with open('members.json', 'w') as fp:
        json.dump(data, fp, indent=2)

# user authentication via Discord command !auth [netid]

@bot.command(name='auth')
async def auth(ctx: commands.Context, *, netid=None):
    if netid is None:
        response = f"{ctx.message.author.mention} Please enter a valid UTK NetID!"
        await ctx.send(response)
        return

    passkey = ''.join([str(number) for number in np.random.randint(10, size=6)])
    auth_pair = {ctx.message.author.id: passkey}
    update_members(auth_pair)
    response = f"{ctx.message.author.mention} Check your UTK email and enter the code received into the chat."
    await ctx.send(response)

bot.run(TOKEN)
