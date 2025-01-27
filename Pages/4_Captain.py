import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# LINK TIL GSHEET PÅ GOOGLE DREV
url = "https://docs.google.com/spreadsheets/d/1oh4NIxUlJH8Y11OQV4GC_G3IWbaqD7FUfrVwUBTMGOE/edit?usp=sharing"

# FORBINDELSE TIL SHEET
conn = st.connection("gsheets", type=GSheetsConnection)

# DANNELSE AF DATA
data = conn.read(spreadsheet=url, worksheet="0")

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Rename Kolonne3 to TripplePointsCaptain
df = df.rename(columns={"Kolonne3": "TripplePointsCaptain"})

# Ensure PointsCaptainHalf and TripplePointsCaptain are numeric for summation
df["PointsCaptainHalf"] = pd.to_numeric(df["PointsCaptainHalf"], errors="coerce")
df["TripplePointsCaptain"] = pd.to_numeric(df["TripplePointsCaptain"], errors="coerce")

# Group by Captain and sum PointsCaptainHalf and TripplePointsCaptain
captain_points = df.groupby("Captain")[["PointsCaptainHalf", "TripplePointsCaptain"]].sum().reset_index()

# Add a column for the total points from PointsCaptainHalf and TripplePointsCaptain
captain_points["Total Points"] = captain_points["PointsCaptainHalf"] + captain_points["TripplePointsCaptain"]

# Display the table
st.title("Captain's Points Summary")
st.table(captain_points)
