import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# 1. Get a fresh ACCESS TOKEN using your REFRESH TOKEN
auth_url = "https://www.strava.com/oauth/token"
payload = {
    'client_id': os.getenv('STRAVA_CLIENT_ID'),
    'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
    'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN'),
    'grant_type': 'refresh_token'
}

print("Requesting fresh access token...")
res = requests.post(auth_url, data=payload)
access_token = res.json()['access_token']

# 2. Use that access token to get activities
activities_url = "https://www.strava.com/api/v3/athlete/activities"
header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 5, 'page': 1}

print("Fetching activities...")
my_dataset = requests.get(activities_url, headers=header, params=param).json()

# 3. Show the results in a nice table
df = pd.DataFrame(my_dataset)
print(df[['name', 'type', 'distance', 'start_date']])