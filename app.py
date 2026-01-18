import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd
import requests
import os

st.set_page_config(page_title="My Strava Dashboard", layout="wide")

# 1. Connect to Supabase
conn = st.connection("supabase", type=SupabaseConnection)

# 2. Function to fetch data from Strava (The "Refresh" Logic)
def refresh_strava_data():
    with st.spinner("🔄 Fetching new activities from Strava..."):
        # This is the same logic we used in your script
        auth_url = "https://www.strava.com/oauth/token"
        payload = {
            'client_id': st.secrets["connections"]["supabase"]["STRAVA_CLIENT_ID"],
            'client_secret': st.secrets["connections"]["supabase"]["STRAVA_CLIENT_SECRET"],
            'refresh_token': st.secrets["connections"]["supabase"]["STRAVA_REFRESH_TOKEN"],
            'grant_type': 'refresh_token'
        }
        res = requests.post(auth_url, data=payload).json()
        access_token = res['access_token']
        
        header = {'Authorization': 'Bearer ' + access_token}
        activities = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=header).json()
        
        for act in activities:
            data = {"id": act['id'], "name": act['name'], "distance": act['distance'], 
                    "type": act['type'], "start_date": act['start_date']}
            conn.table("activities").upsert(data).execute()
        
        st.success("✅ Dashboard Updated!")

# --- DASHBOARD UI ---
st.title("🏃 My Personal Strava Analytics")

# Side bar for the refresh button
with st.sidebar:
    if st.button("🔄 Sync with Strava"):
        refresh_strava_data()

# 3. Pull data from Supabase to show on screen
df_data = conn.table("activities").select("*").execute()
df = pd.DataFrame(df_data.data)

if not df.empty:
    # Quick calculations
    total_distance = df['distance'].sum() / 1000  # Convert meters to km
    
    # Create Columns for "Key Metrics"
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Distance", f"{total_distance:.1f} km")
    col2.metric("Total Activities", len(df))
    col3.metric("Favorite Sport", df['type'].mode()[0])

    # A simple chart
    st.subheader("Activity Distances over Time")
    df['start_date'] = pd.to_datetime(df['start_date'])
    st.line_chart(df.set_index('start_date')['distance'])
    
    # Show the raw data
    st.subheader("Recent Sessions")
    st.dataframe(df)
else:
    st.warning("No data found. Click the Sync button in the sidebar!")