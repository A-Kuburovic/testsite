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

# Ensure necessary columns are numeric
df["Points_after_negative2"] = pd.to_numeric(df["Points_after_negative2"], errors="coerce")
df["Points on bench"] = pd.to_numeric(df["Points on bench"], errors="coerce")

# TITEL
st.title("Overlapping Points for Selected Teams")

# Get the list of unique teams
teams = df["Team"].unique()

# Create the first dropdown for team 1 selection
selected_team_1 = st.selectbox("Select Team 1", options=teams)

# Filter data for the selected team 1
team_1_data = df[df["Team"] == selected_team_1]

# Reshape the data for team 1
team_1_data_melted = team_1_data.melt(
    id_vars=["Uge"], 
    value_vars=["Points_after_negative2", "Points on bench"],
    var_name="Points Type", 
    value_name="Points"
)

# Create the overlapping bar chart for Team 1
chart_team_1 = alt.Chart(team_1_data_melted).mark_bar().encode(
    x=alt.X("Uge:O", title="Week", axis=alt.Axis(grid=False)),
    y=alt.Y("Points:Q", title="Points", axis=alt.Axis(grid=False), stack=None),  # No stacking here
    color=alt.Color("Points Type:N", scale=alt.Scale(domain=["Points_after_negative2", "Points on bench"],
                                                     range=["#29E1FF", "#37003C"]),
                    title="Points Type", legend=None),
    tooltip=["Uge", "Points", "Points Type"]
).properties(
    title=f"Points After Negative for {selected_team_1}"
)

# Display the chart for Team 1
st.altair_chart(chart_team_1, use_container_width=True)

# Create the second dropdown for team 2 selection
selected_team_2 = st.selectbox("Select Team 2", options=teams)

# Filter data for the selected team 2
team_2_data = df[df["Team"] == selected_team_2]

# Reshape the data for team 2
team_2_data_melted = team_2_data.melt(
    id_vars=["Uge"], 
    value_vars=["Points_after_negative2", "Points on bench"],
    var_name="Points Type", 
    value_name="Points"
)

# Create the overlapping bar chart for Team 2
chart_team_2 = alt.Chart(team_2_data_melted).mark_bar().encode(
    x=alt.X("Uge:O", title="Week", axis=alt.Axis(grid=False)),
    y=alt.Y("Points:Q", title="Points", axis=alt.Axis(grid=False), stack=None),  # No stacking here
    color=alt.Color("Points Type:N", scale=alt.Scale(domain=["Points_after_negative2", "Points on bench"],
                                                     range=["#29E1FF", "#37003C"]),
                    title="Points Type", legend=None),
    tooltip=["Uge", "Points", "Points Type"]
).properties(
    title=f"Points After Negative for {selected_team_2}"
)

# Display the chart for Team 2
st.altair_chart(chart_team_2, use_container_width=True)
