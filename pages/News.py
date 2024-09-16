import streamlit as st
from utils import *
from dotenv import load_dotenv
import json
from pathlib import Path
import tempfile 
# from crew.crew_kickoffs import KickoffAgent



with st.sidebar:
    max_news =  st.slider("Select The Max NO Of News Article",min_value=1,max_value=100,step=1,value=30)
    freshness=st.selectbox("Select news Freshness ['Day', 'Week','Month'] ",['Day', 'Week','Month'])
    sort_by=st.selectbox("Sort By ['RelevanceRanking', 'Date'] ",["Relevance", 'Date'])
    search_term =  st.text_input(label="Search News",placeholder="Search News",max_chars=100,)
    
    

if search_term:
    if st.button("Click to Search News "):
        tab1, tab2 = st.tabs(["GNews", "Bing News Search API"])
        json_file_search_term_name = search_term.replace(' ', '_')
        with tab1:
            get_news_and_put_download_button("GNews",search_term,freshness,max_news,sort_by)
        with tab2:
            get_news_and_put_download_button("Bing News Search API",search_term,freshness,max_news,sort_by)
        # with tab3:
        #     get_news_and_put_download_button("Google + Bing",search_term,freshness,max_news,sort_by)

else:
    st.subheader("Please Enter What you want to search")

            
            

            
