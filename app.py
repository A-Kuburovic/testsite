import streamlit as st

#st.title("Super Duper League")

#DATA_FILE_2 = "Fantasy.xlsx"

# --- PAGE SETUP ---
League_Tables = st.Page(
    page="views/LeagueTables.py",
    title="League Tables",
    icon="📊",
    default=True,
)

Teams_Tables = st.Page(
    page="views/TeamsTables.py",
    title="Teams Tables",
    icon="💕",

)

Data_Source = st.Page(
    page="views/DataSource.py",
    title="Data Source",
    icon="😎",

)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
pg = st.navigation(pages=[League_Tables, Teams_Tables, Data_Source])

# --- RUN NAVIGATION ---
pg.run()