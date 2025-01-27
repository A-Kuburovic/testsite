import streamlit as st
import pandas as pd
import altair as alt
from streamlit_gsheets import GSheetsConnection

# LINK TIL GSHEET PÅ GOOGLE DREV
url = "https://docs.google.com/spreadsheets/d/1oh4NIxUlJH8Y11OQV4GC_G3IWbaqD7FUfrVwUBTMGOE/edit?usp=sharing"

# FORBINDELSE TIL SHEET
conn = st.connection("gsheets", type=GSheetsConnection)

# DANNELSE AF DATA
data = conn.read(spreadsheet=url, worksheet="0")

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Ensure "Gameweek points" is numeric for summation
df["Gameweek points"] = pd.to_numeric(df["Gameweek points"], errors="coerce")

# TITEL
st.title("Gameweek Points over Uge by Team")

# Get a list of unique teams
teams = df["Team"].unique()

# Create a multiselect widget to choose teams
selected_teams = st.multiselect("Select Teams", options=teams, default=teams)

# Filter the data based on selected teams
filtered_data = df[df["Team"].isin(selected_teams)]

# Group by Uge and Team, and sum the Gameweek points
weekly_points = (
    filtered_data.groupby(["Uge", "Team"])["Gameweek points"]
    .sum()
    .reset_index()
)

# Create a line chart with Altair
line_chart = alt.Chart(weekly_points).mark_line().encode(
    x=alt.X("Uge:O", title="Uge"),  # Treat Uge as ordinal (categorical)
    y=alt.Y("Gameweek points:Q", title="Gameweek Points", axis=alt.Axis(grid=False)),
    color="Team:N",  # Different color for each team
    tooltip=["Team", "Uge", "Gameweek points"]
)

# Display the line chart
st.altair_chart(line_chart, use_container_width=True)
