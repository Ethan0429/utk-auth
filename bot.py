#!/usr/bin/python3
# bot.py
from discord.ext import commands
from discord.utils import get
import canvas_utils
import utk_mail
import bot_utils
import bot_vars
import os

bot = commands.Bot(command_prefix='!')

# add auth role to user
async def assign_role(user):
    print(f'assigning auth role to {str(user.name)}...')
    if bot_utils.is_auth(user):
        print(f'{str(user.name)} already has auth role!')
        return
    role = get(user.guild.roles, name=bot_vars.auth_role)
    await user.add_roles(role)

@bot.event
async def on_ready(): 
    open('members.json', 'w').close()
    bot_vars.users = canvas_utils.get_student_names()
    print(f'{bot.user} is online!') 

# user authentication via Discord command !auth [netid]
@bot.command(name='auth')
async def auth(ctx: commands.Context, *, netid=None):
    print('\nauthenticating...')
    member = ctx.message.author
    str_member_id = str(member.id)
    if bot_utils.is_auth(member):
        return
    if netid is None:
        print(f'netid invalid!')
        await ctx.send(f'{member.mention} Please enter a valid UTK NetID!')
        return
    if bot_utils.key_exists(str_member_id):
        print(f'{netid} already has an authid!')
        await ctx.send(f'{member.mention} there already exists a passcode for this NetID. Type `!reset` to reset your passcode.')
        return

    auth_id = bot_utils.generate_auth_id(str_member_id, str(netid))
    bot_utils.update_members(auth_id)
    await utk_mail.send_auth_email(auth_id) # send passkey email
    response = f'{member.mention} Check your UTK email **(SPAM FOLDER)** and enter the code received into the chat.'
    await ctx.send(response)

# read passkey for valid match
@bot.command(name='verify')
async def verify(ctx: commands.Context, *, passkey: str):
    print('\nverifying...')
    member = ctx.message.author
    str_member_id = str(member.id)
    if bot_utils.is_auth(member):
        return

    auth_id = await bot_utils.get_auth_id(str_member_id)

    # if passkey matches members.json, assign Student role and confirm authentication
    if passkey == auth_id['passkey']:
        await ctx.message.channel.send(f'{member.mention} Authentication succesful!')
        bot_utils.remove_member(str_member_id)
        await assign_role(member)
        await member.edit(nick=bot_vars.users[auth_id['netid']])
    return

# resets passkey if it already exists in members.json
@bot.command(name='reset')
async def reset(ctx: commands.Context):
    member = ctx.message.author
    str_member_id = str(member.id)
    print(f'\nresetting {str_member_id} authid...')

    if bot_utils.is_auth(member):
        await ctx.send(f'{member.mention} you\'re already authorized!')
        return
    if await bot_utils.get_auth_id(str_member_id) == None:
        await ctx.send(f'{member.mention} there is no code on file for your discord account!\nRun `!auth [netid]` (without brackets) command for starting the authentication process')
        return
    bot_utils.remove_member(str_member_id)
    await ctx.send(f'{member.mention} your passcode has been reset!')
    return

bot.run(bot_vars.TOKEN)
