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
st.title("Average Gameweek Points by Week")

# Group by "Uge" and calculate the sum of "Gameweek points" for each combination of "Uge" and "Team"
weekly_points = df.groupby(["Uge", "Team"])["Gameweek points"].sum().reset_index()

# Calculate the average of Gameweek points per week by dividing the sum by the number of unique teams for each week
average_weekly_points = (
    weekly_points.groupby("Uge")["Gameweek points"]
    .mean()
    .reset_index()
)

# Calculate the overall average of "Gameweek points"
average_points = average_weekly_points["Gameweek points"].mean()

# Create a bar chart with Altair
bars = alt.Chart(average_weekly_points).mark_bar(color="#29E1FF").encode(
    x=alt.X("Uge:O", title="Week", axis=alt.Axis(grid=False)),  # Remove gridlines from x-axis
    y=alt.Y("Gameweek points:Q", title="Average Gameweek Points", axis=alt.Axis(grid=False)),  # Remove gridlines from y-axis
    tooltip=["Uge", "Gameweek points"]
)

# Add a line for the average of all weeks with custom color
average_line = alt.Chart(pd.DataFrame({"Uge": [average_weekly_points["Uge"].min(), average_weekly_points["Uge"].max()], 
                                      "Gameweek points": [average_points, average_points]})).mark_line(
    color="#02F7C8", size=2, strokeDash=[5, 5]
).encode(
    x="Uge:O",
    y="Gameweek points:Q"
)

# Combine the bar chart and the average line
chart = bars + average_line

# Display the chart
st.altair_chart(chart, use_container_width=True)
