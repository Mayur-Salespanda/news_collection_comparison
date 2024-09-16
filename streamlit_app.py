import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_navigation_bar import st_navbar
from utils import initialize_session
load_dotenv()
initialize_session()
print(os.getenv("ANTHROPIC_API_KEY"))
page = st_navbar(["Home","News", "Report Genration", "Settings"],options={"show_sidebar":True,"hide_nav":False})

if page == "News":
    st.switch_page("pages/News.py")
if page == "Settings":
    st.switch_page("pages/Settings.py")


st.header('POC on news gathering')