import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import altair as alt

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

# CaptainsUsed: Unique names, count of appearances, and sum of points
captains_used = df.groupby("Captain").agg(
    Count=('Captain', 'size'),
    Total_Points=('PointsCaptain', 'sum')
).reset_index()

# TITEL
st.title("Fantasy Football Analytics")

# Chart 1: CaptainsUsed
captains_chart = alt.Chart(captains_used).mark_bar().encode(
    x=alt.X('Total_Points:Q', title='Total Points'),
    y=alt.Y('Captain:N', sort='-x', title='Captain'),
    tooltip=['Captain', 'Count', 'Total_Points']
).properties(title="Captains Used")

st.altair_chart(captains_chart)

# LeaguePodium: Top 13 teams by Gameweek points
top_teams_all = df.groupby("Team")["Gameweek points"].sum().reset_index()
top_teams_all = top_teams_all.sort_values(by="Gameweek points", ascending=False)

# Chart 2: Top 13 Teams by Gameweek Points
league_podium_chart_all = alt.Chart(top_teams_all).mark_bar(color='#29E1FF').encode(
    x=alt.X("Gameweek points:Q", title="Total Gameweek Points"),
    y=alt.Y("Team:N", sort='-x', title="Team"),
    tooltip=["Team", "Gameweek points"]
).properties(title="Top 13 Teams by Gameweek Points")

st.altair_chart(league_podium_chart_all)

# NumberOfPlaces: Most points for each "Uge"
points_per_uge = df.groupby(["Uge", "Team"])["Gameweek points"].sum().reset_index()
best_in_uge = points_per_uge.loc[points_per_uge.groupby('Uge')['Gameweek points'].idxmax()]

# Chart 3: Best Points by Uge (Ascending order)
best_in_uge_chart = alt.Chart(best_in_uge).mark_bar(color='#29E1FF').encode(
    x=alt.X("Gameweek points:Q", title="Total Points"),
    y=alt.Y("Uge:N", sort='ascending', title="Uge"),
    color="Team:N",
    tooltip=["Uge", "Team", "Gameweek points"]
).properties(title="Best Points by Uge")

st.altair_chart(best_in_uge_chart)

# Original chart: Total Points by Team
team_points = (
    df.groupby("Team")["Gameweek points"]
    .sum()
    .reset_index()
    .dropna()
    .sort_values(by="Gameweek points", ascending=False)
)

team_points = team_points.reset_index(drop=True).reset_index()
team_points["index"] += 1

team_points.columns = ["Count", "Team", "Total Points"]
team_points["Total Points"] = team_points["Total Points"].astype(int)

# Create a sideways bar chart using Altair with values displayed and custom color
bars = alt.Chart(team_points).mark_bar(color="#29E1FF").encode(
    x=alt.X("Total Points:Q", title="Total Points"),
    y=alt.Y("Team:N", sort="-x", title="Team"),
    tooltip=["Team", "Total Points"]
)

text = bars.mark_text(
    align="left",
    baseline="middle",
    dx=3,  # Offset text slightly from the bar
    color="#02F7C8"  # Set the text color
).encode(
    text=alt.Text("Total Points:Q")
)

bar_chart = (bars + text).properties(
    title="Total Points by Team",
    height=400,
    width=600
)

st.altair_chart(bar_chart, use_container_width=True)

# Chart 4: OverallRankGameWeek
overall_rank_gameweek = df.groupby(["Gameweek", "Overall_rank"]).size().reset_index(name='Count')
overall_rank_gameweek_chart = alt.Chart(overall_rank_gameweek).mark_bar(color='#29E1FF').encode(
    x=alt.X("Gameweek:O", title="Gameweek"),
    y=alt.Y("Count:Q", title="Count of Teams"),
    color="Overall_rank:N",
    tooltip=["Gameweek", "Overall_rank", "Count"]
).properties(title="Overall Rank by Gameweek")
st.altair_chart(overall_rank_gameweek_chart)

# Chart 5: MinAndMaxPointsToDate
min_max_points = df.groupby("Team").agg(
    MinPoints=('Overall point', 'min'),
    MaxPoints=('Overall point', 'max')
).reset_index()

min_max_points_chart = alt.Chart(min_max_points).mark_bar().encode(
    x=alt.X("MinPoints:Q", title="Min Points"),
    y=alt.Y("Team:N", title="Team"),
    color="Team:N",
    tooltip=["Team", "MinPoints", "MaxPoints"]
).properties(title="Min and Max Points to Date")
st.altair_chart(min_max_points_chart)

# Chart 6: AveragePointsOnBenchPerGameWeek
avg_bench_points = df.groupby("Gameweek")["Points on bench"].mean().reset_index()
avg_bench_points_chart = alt.Chart(avg_bench_points).mark_line(color='#29E1FF').encode(
    x=alt.X("Gameweek:O", title="Gameweek"),
    y=alt.Y("Points on bench:Q", title="Average Points on Bench"),
    tooltip=["Gameweek", "Points on bench"]
).properties(title="Average Points on Bench Per Gameweek")
st.altair_chart(avg_bench_points_chart)

# Chart 7: TrippleCaptainPointsAndCaptainPoints
triple_and_captain_points = df.groupby("Gameweek").agg(
    TripleCaptainPoints=('TrippleCaptain', 'sum'),
    CaptainPoints=('PointsCaptain', 'sum')
).reset_index()

triple_and_captain_points_chart = alt.Chart(triple_and_captain_points).mark_line().encode(
    x=alt.X("Gameweek:O", title="Gameweek"),
    y=alt.Y("TripleCaptainPoints:Q", title="Triple Captain Points"),
    color="TripleCaptainPoints:N",
    tooltip=["Gameweek", "TripleCaptainPoints", "CaptainPoints"]
).properties(title="Triple Captain and Captain Points")
st.altair_chart(triple_and_captain_points_chart)

# Chart 8: NegativePointsGameWeek
negative_points_gameweek = df.groupby("Gameweek")["Point_negative"].sum().reset_index()
negative_points_gameweek_chart = alt.Chart(negative_points_gameweek).mark_bar(color='#29E1FF').encode(
    x=alt.X("Gameweek:O", title="Gameweek"),
    y=alt.Y("Point_negative:Q", title="Negative Points"),
    tooltip=["Gameweek", "Point_negative"]
).properties(title="Negative Points Per Gameweek")
st.altair_chart(negative_points_gameweek_chart)

# Chart 9: NegativePointsTotal
negative_points_total = df.groupby("Team")["Point_negative"].sum().reset_index()
negative_points_total_chart = alt.Chart(negative_points_total).mark_bar(color='#29E1FF').encode(
    x=alt.X("Point_negative:Q", title="Total Negative Points"),
    y=alt.Y("Team:N", sort='-x', title="Team"),
    tooltip=["Team", "Point_negative"]
).properties(title="Total Negative Points by Team")
st.altair_chart(negative_points_total_chart)

# Chart 10: LowerstAndHighestsGameWeekRank
lowest_highest_gameweek_rank = df.groupby("Gameweek").agg(
    MinRank=('Gameweek rank', 'min'),
    MaxRank=('Gameweek rank', 'max')
).reset_index()

lowest_highest_gameweek_rank_chart = alt.Chart(lowest_highest_gameweek_rank).mark_bar().encode(
    x=alt.X("MinRank:Q", title="Minimum Rank"),
    y=alt.Y("Gameweek:O", title="Gameweek"),
    color="Gameweek:N",
    tooltip=["Gameweek", "MinRank", "MaxRank"]
).properties(title="Lowest and Highest Gameweek Rank")
st.altair_chart(lowest_highest_gameweek_rank_chart)

# Chart 11: LowestAndHighestOverallRank
lowest_highest_overall_rank = df.groupby("Team").agg(
    MinRankOverall=('Overall_rank', 'min'),
    MaxRankOverall=('Overall_rank', 'max')
).reset_index()

lowest_highest_overall_rank_chart = alt.Chart(lowest_highest_overall_rank).mark_bar().encode(
    x=alt.X("MinRankOverall:Q", title="Minimum Overall Rank"),
    y=alt.Y("Team:N", sort='-x', title="Team"),
    color="Team:N",
    tooltip=["Team", "MinRankOverall", "MaxRankOverall"]
).properties(title="Lowest and Highest Overall Rank")
st.altair_chart(lowest_highest_overall_rank_chart)
