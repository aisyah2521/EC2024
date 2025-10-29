import streamlit as st

st.set_page_config(
    page_title="Student Survey"
)

visualise = st.Page('Student survey.py', title='Pencapaian Akademik', icon=":material/school:")

home = st.Page('Home.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
    {
        "Menu": [home, visualise]
    }
)

pg.run()   
