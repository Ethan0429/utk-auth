# bot.py
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

# acccesses bot email credentials used for user authentication

def get_credentials():
    return os.getenv('BOT_EMAIL_USER'), os.getenv('BOT_EMAIL_PASS')

# user authentication via Discord command !auth [netid]

@bot.command(name='auth')
async def auth(ctx: commands.Context, *, netid):
    if netid is None:
        await ctx.send("Please enter a valid UTK NetID!")
        return
    response = f"{ctx.message.author.mention} Check your UTK email and enter the code received into the chat."
    await ctx.send(response)

bot.run(TOKEN)
