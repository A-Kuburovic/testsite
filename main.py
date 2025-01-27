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
st.title("Gameweek Points by Team")

# Get a list of unique teams
teams = df["Team"].unique()

# Create a multiselect widget to choose teams
selected_teams = st.multiselect("Select Teams", options=teams, default=teams)

# Filter the data based on selected teams
filtered_data = df[df["Team"].isin(selected_teams)]

# Group by Team and calculate the sum of Gameweek points
team_points = (
    filtered_data.groupby("Team")["Gameweek points"]
    .sum()
    .reset_index()
    .sort_values(by="Gameweek points", ascending=False)
)

# Create a bar chart with Altair
bars = alt.Chart(team_points).mark_bar(color="#29E1FF").encode(
    x=alt.X("Gameweek points:Q", title="Gameweek Points", axis=alt.Axis(grid=False)),
    y=alt.Y("Team:N", sort="-x", title="Team", axis=alt.Axis(grid=False)),
    tooltip=["Team", "Gameweek points"]
)

# Add the text labels inside the bars
text = bars.mark_text(
    align="right",  # Center the text inside the bar
    baseline="middle",
    dx=0,  # Centered within the bar
    color="#37003C",  # Set the text color
    fontWeight="bold",
    fontSize=16
).encode(
    text=alt.Text("Gameweek points:Q")
)

# Combine the bars and text
bar_chart = (bars + text).properties(
    title="Gameweek Points by Team",
    height=700,  # Adjust the height of the chart
    width=600    # Adjust the width of the chart
)

# Display the bar chart
st.altair_chart(bar_chart, use_container_width=True)
