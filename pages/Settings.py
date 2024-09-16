import streamlit as st
from constant import *






with st.container(border=True):
    index = 0
    sort_by = None
    session_sort_by_choice = st.session_state.get(SESSION_SORT_NEWS_BY_KEY)
    if session_sort_by_choice:
        index = ["Relevance", 'Date'].index(session_sort_by_choice)
    sort_by=st.selectbox("Sort By ['RelevanceRanking', 'Date'] ",["Relevance", 'Date'],index)
    st.session_state[SESSION_SORT_NEWS_BY_KEY]=sort_by
        
    
    
    

