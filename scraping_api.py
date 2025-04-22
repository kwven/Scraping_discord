import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
EMAIL = os.getenv("EMAIL")
SERVER_ID = os.getenv("SERVER_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# the Authorization header format
h = {'Authorization':ACCESS_TOKEN}

# count of server members
def get_member_count(server_id):
    r = requests.get(f'https://discord.com/api/guilds/{server_id}/preview', headers=h)
    j = json.loads(r.text)
    return j['approximate_member_count']


# count of currently online server members
def get_presence_count(server_id):
    req = requests.get(f'https://discord.com/api/guilds/{server_id}/preview', headers=h)
    jl = json.loads(req.text)
    return jl['approximate_presence_count']


def get_last_15_messages_from_channel(channel_id):
    req = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=15', headers=h)
    jl = json.loads(req.text)
    m = [c['content'] for c in jl]
    return m

print(get_presence_count(SERVER_ID))
print(get_member_count(SERVER_ID))
print(get_last_15_messages_from_channel(CHANNEL_ID))