#!/usr/bin/python3
# bot.py
import canvas_utils
import utk_mail
import bot_utils
import bot_vars
import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
import os
import asyncio

# global vars
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


async def send_async_response(interaction, full_name, assignment):
    sd = canvas_utils.StudentDashboard()
    data = await sd.get_student_info(username=full_name)
    canvas_utils.save_student_info_to_md(data)

    if assignment is None:
        message = canvas_utils.return_student_header(data)
        bot_utils.md_to_png(
            f'{data["student_name"]}.png', canvas_utils.return_student_header(data))
        message = "Generated student info image"
        # Attach the generated image and send it as a message.
        with open(f'{data["student_name"]}.png', 'rb') as file:
            image = discord.File(file, f'{data["student_name"]}.png')
        await interaction.channel.send(message, file=image)
    else:
        found_assignment = bot_utils.find_closest_assignment(data, assignment)
        bot_utils.md_to_png(f'{data["student_name"]}.png', canvas_utils.return_assignment_info(
            data, found_assignment))
        message = f"Generated assignment info image\n\n**Links**:\nAssignment URL: {found_assignment['submission']['url']}\nSubmission URL: {found_assignment['submission']['submission_url']}"
        # Attach the generated image and send it as a message.
        with open(f'{data["student_name"]}.png', 'rb') as file:
            image = discord.File(file, f'{data["student_name"]}.png')
        await interaction.channel.send(message, file=image)

    # Clean up generated image file
    if os.path.exists(f'{data["student_name"]}.png'):
        os.remove(f'{data["student_name"]}.png')

# add auth role to user


async def assign_role(member: discord.Member):
    print(f'assigning auth role to {str(member.name)}...')
    if bot_utils.is_auth(member):
        print(f'{str(member.name)} already has auth role!')
        return
    role = get(member.guild.roles, name=bot_vars.auth_role)
    await member.add_roles(role)

# user authentication via Discord command /auth [netid]


@bot.tree.command(name='auth', description='Sends authentication email', guild=discord.Object(id=bot_vars.CONST_COSC102_GUILD_ID))
async def auth(interaction: discord.Interaction, netid: str):
    print('\nauthenticating...')
    member = interaction.user
    id = str(member.id)
    if bot_utils.is_auth(member):
        await interaction.response.send_message(f'{member.mention} You\'re already authenticated. Nothing to see here!', ephemeral=True)
        return
    if netid is None:
        print(f'netid invalid!')
        await interaction.response.send_message(f'{member.mention} Please enter a valid UTK NetID!', ephemeral=True)
        return
    if bot_utils.key_exists(id):
        print(f'{netid} already has an authid!')
        await interaction.response.send_message(f'{member.mention} there already exists a passcode for this NetID. Type `/reset` to reset your passcode.', ephemeral=True)
        return

    auth_id = bot_utils.generate_auth_id(id, str(netid))
    bot_utils.update_members(auth_id)
    await utk_mail.send_auth_email(auth_id)  # send passkey email
    gmail_response = f'If you\'re using Gmail, check your **spam folder**'
    outlook_response = f'If you\'re using Outloozk, check your **quarantine folder** or click this link https://security.microsoft.com/quarantine'
    embed = discord.Embed(title=f'Verification code sent!', description=f'{member.mention} Check your UTK email\'s **spam** inbox and follow the instructions written.', color=0xFFCC00, type='rich').add_field(
        name='Gmail', value=gmail_response, inline=False).add_field(name='Outlook', value=outlook_response, inline=False)
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
        print(f'{str(member.name)} Authentication successful!')
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

# create a command that iterates through each member in the server and checks the date they joined, then kicks them if they are too old


@bot.tree.command(name='kick_old', description='Kicks old users', guild=discord.Object(id=bot_vars.CONST_COSC102_GUILD_ID), )
async def kick_old(interaction: discord.Interaction):
    # make sure the user who sent the command is an admin
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(f'{interaction.user.mention} You do not have permission to use this command!', ephemeral=True)
        return

    print('\nchecking...')
    users = []
    # iterate through each member in the server, only add members who joined before the year 2023 AND that have no roles
    for member in interaction.guild.members:
        if member.joined_at.year < 2023 and len(member.roles) == 1:
            users.append(member)

    users_string = '\n'.join([user.name for user in users])

    # send a message of all the users that will be kicked
    await interaction.response.send_message(f'{interaction.user.mention} The following users will be kicked: {users_string}\nAre you sure you want to kick these users? (y/n)', ephemeral=True)

    # await the user to confirm the kick
    response = await bot.wait_for('message', check=lambda message: message.author == interaction.user)
    if response.content.lower() != 'y':
        await interaction.channel.send(content=f'{interaction.user.mention} Kicking cancelled!', delete_after=5)
        return

    # kick each user in the list
    for user in users:
        await user.kick(reason='2023 semester')
        print(f'{user.name} kicked!')


async def full_names_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:

    with open('student_names.txt', 'r') as f:
        choices = f.read().splitlines()

    return [
        app_commands.Choice(name=choice, value=choice)
        for choice in choices if current.lower() in choice.lower()
    ]


@bot.tree.command(name='canvas', description='Gets Canvas info for a user.', guild=discord.Object(id=bot_vars.CONST_COSC102_GUILD_ID))
@app_commands.autocomplete(full_names=full_names_autocomplete)
async def canvas(interaction: discord.Interaction, full_names: str, assignment: str = None):
    # make sure the user who sent the command is an admin or has role id 935991929978621966
    if not interaction.user.guild_permissions.administrator or discord.utils.get(interaction.user.roles, id=bot_vars.CONST_COSC102_TA_ROLE_ID) is None:
        await interaction.response.send_message(f'{interaction.user.mention} You do not have permission to use this command!', ephemeral=True)
        return

    # Acknowledge the command immediately
    await interaction.response.send_message(f'Processing your request, {interaction.user.mention}. Please wait...', ephemeral=True)

    # Create a separate task to handle the API request and send the response when ready
    asyncio.create_task(send_async_response(
        interaction, full_names, assignment))


@ bot.event
async def on_ready():
    open('members.json', 'w').close()
    _, bot_vars.users = canvas_utils.get_student_names()

    print("syncing...")
    await bot.tree.sync(guild=discord.Object(id=bot_vars.CONST_COSC102_GUILD_ID))
    print(f'{bot.user} is online!')

bot.run(bot_vars.TOKEN)
