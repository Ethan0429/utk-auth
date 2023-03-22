import bot_vars
import json
import numpy as np
import discord
from bot_vars import AuthID
import difflib
from PIL import Image
import markdown
import imgkit
import asyncio

# check if a key already exists


def key_exists(user):
    print(f'checking if key exists for {user}...')
    data = {}  # json dict placeholder
    try:  # if members.json is not empty...
        with open('members.json', 'r') as f:
            data = json.load(f)              # read dict into data
    except json.JSONDecodeError:
        return False

    if user in data:
        return True
    return False

# updates member list for auth tracking


def update_members(auth_id):
    print('adding new member...')
    data = {
        auth_id.member_id:
        {
            'passkey': auth_id.passkey,
            'netid': auth_id.netid
        }
    }
    try:  # if members.json is not empty...
        with open('members.json') as f:
            new_data = json.load(f)  # read dict into data
            data = new_data
    except json.JSONDecodeError as e:
        print(e)
        pass

    with open('members.json', 'w') as f:
        data[auth_id.member_id] = {
            'passkey': auth_id.passkey,
            'netid': auth_id.netid
        }
        print(data)
        json.dump(data, f, indent=2)


def remove_member(user):
    print(f'removing {user}...')
    data = {}
    try:
        with open('members.json') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pass

    with open('members.json', 'w') as f:
        data.pop(user, None)
        json.dump(data, f, indent=2)
        print(f'{user} passkey removed from members.json!')

# return passkey mapped to user ID from members.json


async def get_auth_id(user):
    print(f'retrieving {user} passkey...')
    f = open('members.json', 'r')
    data = json.load(f)
    f.close()
    print(data)
    if user in data:
        print(f'{user} passkey found!')
        return data[user]
    else:
        print(f'no passkey for {user} in members.json!')

# check is user is already authenticated (has Student role)


def is_auth(member: discord.Member):
    print('checking authorization status...')
    if member.get_role(bot_vars.auth_role_id) != None:
        print(f'{member} is already authenticated!')
        return True
    print(f'{member} has not been authenticated!')
    return False


def generate_auth_id(member_id, netid):
    print(f'init member-id and passkey for {netid}...')
    # generate passkey
    passkey = ''.join([str(number)
                      for number in np.random.randint(10, size=6)])
    auth_id = AuthID(member_id, passkey, netid)
    return auth_id


def find_closest_assignment(data, user_input, n=1, cutoff=0.1):
    user_input_lower = user_input.lower()
    assignment_names = [(assignment, assignment["name"].lower())
                        for assignment in data["assignments"]]
    assignment_names_lower = [name_lower for _, name_lower in assignment_names]

    close_matches = difflib.get_close_matches(
        user_input_lower, assignment_names_lower, n=n, cutoff=cutoff)

    if close_matches:
        closest_match_lower = close_matches[0]
        matching_assignment = [assignment for assignment,
                               _ in assignment_names if assignment["name"].lower() == closest_match_lower][0]
        return matching_assignment
    else:
        return None


def md_to_png(filename, md_string):
    html = markdown.markdown(md_string)

    wrapped_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: auto;
                padding: 2rem;
            }}
        </style>
    </head>
    <body>
    {html}
    </body>
    </html>
    """

    imgkit.from_string(wrapped_html, filename)
