import requests
import os
from dotenv import load_dotenv

# This tells Python to look specifically in the current folder for the .env file
load_dotenv(override=True) 

def get_env_var(name):
    value = os.getenv(name)
    if value is None:
        print(f"❌ ERROR: Variable '{name}' not found in your .env file!")
        return None
    return value.strip()

# Get variables safely
client_id = get_env_var('STRAVA_CLIENT_ID')
client_secret = get_env_var('STRAVA_CLIENT_SECRET')
code = get_env_var('STRAVA_AUTH_CODE')

# Stop the script if any are missing
if not all([client_id, client_secret, code]):
    print("\n⚠️  Please fix your .env file and run again.")
    exit()

print(f"--- Exchange Attempt ---")
url = 'https://www.strava.com/api/v3/oauth/token'
payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
    'grant_type': 'authorization_code'
}

res = requests.post(url, data=payload)

if res.status_code == 200:
    print("✅ SUCCESS!")
    print(f"Your Refresh Token: {res.json()['refresh_token']}")
else:
    print(f"❌ ERROR {res.status_code}: {res.json()}")