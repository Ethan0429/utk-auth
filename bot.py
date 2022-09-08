#!/usr/bin/python3
# bot.py
import canvas_utils
import utk_mail
import bot_utils
import bot_vars
import discord
from discord.ext import commands
from discord.utils import get

# global vars
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# add auth role to user
async def assign_role(member: discord.Member):
    print(f'assigning auth role to {str(member.name)}...')
    if bot_utils.is_auth(member):
        print(f'{str(member.name)} already has auth role!')
        return
    role = get(member.guild.roles, name=bot_vars.auth_role)
    await member.add_roles(role)

@bot.event
async def on_ready(): 
    open('members.json', 'w').close()
    bot_vars.users = canvas_utils.get_student_names()
    await bot.tree.sync(guild=discord.Object(id=bot_vars.CONST_COSC102_GUILD_ID))
    print(f'{bot.user} is online!') 

# user authentication via Discord command !auth [netid]
@bot.tree.command(name='auth', description='Sends authentication email', guild=discord.Object(id=bot_vars.CONST_COSC102_GUILD_ID))
async def auth(interaction: discord.Interaction, netid: str):
    print('\nauthenticating...')
    member = interaction.user
    id = str(member.id)
    if bot_utils.is_auth(member):
        return
    if netid is None:
        print(f'netid invalid!')
        await interaction.response.send_message(f'{member.mention} Please enter a valid UTK NetID!', ephemeral=True)
        return
    if bot_utils.key_exists(id):
        print(f'{netid} already has an authid!')
        await interaction.response.send_message(f'{member.mention} there already exists a passcode for this NetID. Type `!reset` to reset your passcode.', ephemeral=True)
        return

    auth_id = bot_utils.generate_auth_id(id, str(netid))
    bot_utils.update_members(auth_id)
    await utk_mail.send_auth_email(auth_id) # send passkey email
    gmail_response = f'If you\'re using Gmail, check your **spam folder**'
    outlook_response = f'If you\'re using Outlook, check your **quarantine folder** or click this link https://security.microsoft.com/quarantine'
    embed = discord.Embed(title=f'Verification code sent!', description=f'{member.mention} Check your UTK email and enter the code received into the chat', color=0xFFCC00, type='rich').add_field(name='Gmail', value=gmail_response, inline=False).add_field(name='Outlook', value=outlook_response, inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# read passkey for valid match
@bot.tree.command(name='verify', description='Verifies pin from auth email', guild=discord.Object(id=bot_vars.CONST_COSC102_GUILD_ID))
async def verify(interaction: discord.Interaction, passkey: str):
    print('\nverifying...')
    member = interaction.user
    id = str(member.id)
    if bot_utils.is_auth(member):
        return

    auth_id = await bot_utils.get_auth_id(id)

    # if passkey matches members.json, assign Student role and confirm authentication
    if passkey == auth_id['passkey']:
        await interaction.response.send_message(f'{member.mention} Authentication successful!', ephemeral=True)
        bot_utils.remove_member(id)
        await assign_role(member)
        await member.edit(nick=bot_vars.users[auth_id['netid']])
    return

# resets passkey if it already exists in members.json
@bot.tree.command(name='reset', description='Resets verification pin', guild=discord.Object(id=bot_vars.CONST_COSC102_GUILD_ID))
async def reset(interaction: discord.Interaction):
    member = interaction.user
    id = str(member.id)
    print(f'\nresetting {id} authid...')

    if bot_utils.is_auth(member):
        await interaction.response.send_message(f'{member.mention} you\'re already authorized!', ephemeral=True)
        return
    if await bot_utils.get_auth_id(id) == None:
        await interaction.response.send_message(f'{member.mention} there is no code on file for your discord account!\nRun `/auth [netid]` (without brackets) command for starting the authentication process', ephemeral=True)
        return
    bot_utils.remove_member(id)
    await interaction.response.send_message(f'{member.mention} your passcode has been reset!', ephemeral=True)
    return

bot.run(bot_vars.TOKEN)
