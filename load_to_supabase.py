import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client
import requests

load_dotenv()

import datetime

#STEP 1

# 1. Get the exact start of 2026 in UTC
start_2026 = datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)

# 2. Convert to the integer "Epoch" timestamp Strava needs
after_timestamp = int(start_2026.timestamp())

print(f"⏰ Filtering for activities after Epoch: {after_timestamp} (Jan 1, 2026)")

header = {'Authorization': 'Bearer ' + access_token}
params = {
    'after': after_timestamp,
    'per_page': 200 # Get up to 200 activities from this year
}

my_dataset = requests.get(
    "https://www.strava.com/api/v3/athlete/activities", 
    headers=header, 
    params=params
).json()

print(f"✅ Found {len(my_dataset)} activities from 2026.")

# --- PART 2: CONNECT TO SUPABASE ---
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- PART 3: PUSH DATA ---
print("🚀 Uploading to Supabase...")

for activity in my_dataset:
    # We only pick the columns that match our SQL table
    data_to_save = {
        "id": activity['id'],
        "name": activity['name'],
        "distance": activity['distance'],
        "moving_time": activity['moving_time'],
        "type": activity['type'],
        "start_date": activity['start_date']
    }
    
    # This 'upsert' command means: "Insert if new, update if already exists"
    # This prevents errors if you run the script twice!
    response = supabase.table("activities").upsert(data_to_save).execute()

print("✅ All done! Check your Supabase dashboard.")