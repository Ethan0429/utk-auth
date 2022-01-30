import bot_vars
import json
import numpy as np
from bot_vars import AuthID

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
        auth_id.member_id: 
        { 
            'passkey': auth_id.passkey,
            'netid': auth_id.netid
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
        data[auth_id.member_id] = { 
            'passkey': auth_id.passkey,
            'netid': auth_id.netid 
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
    if bot_vars.auth_role in roles:
        print(f'{user} is already authenticated!')
        return True
    return False

def generate_auth_id(member_id, netid):
    passkey = ''.join([str(number) for number in np.random.randint(10, size=6)]) # generate passkey
    auth_id = AuthID(member_id, passkey, netid)
    return auth_id