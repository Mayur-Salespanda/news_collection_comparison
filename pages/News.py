import streamlit as st
from utils import *
from dotenv import load_dotenv
import json
from pathlib import Path
import tempfile 
from datetime import datetime, timedelta
from const import language_codes
# from crew.crew_kickoffs import KickoffAgent


one_month_ago = datetime.now().replace(day=1) - timedelta(days=1) if datetime.now().month == 1 else (datetime.now().replace(day=1) - timedelta(days=1)).replace(month=datetime.now().month - 1)
tab1, tab2,tab3,tab4 = st.tabs(["GNews", "Bing News Search API","News Apis(.org)","News AI(.ai)"])
with tab1:
    max_news =  st.slider("Select The Max NO Of News Article",min_value=1,max_value=100,step=1,value=30)
    freshness=st.selectbox("Select news Freshness ['Day', 'Week','Month'] ",['Day', 'Week','Month'])
    sort_by=st.selectbox("Sort By ['RelevanceRanking', 'Date'] ",["Relevance", 'Date'])
    search_term =  st.text_input(label="Search News",placeholder="Search News",max_chars=100,)
    if search_term: 
        if st.button("Click to Search News ",key="search button 1"):
            get_news_and_put_download_button("GNews",search_term,freshness,max_news,sort_by)
with tab2:
    max_news =  st.slider("Select The Max NO Of News Article.",min_value=1,max_value=100,step=1,value=30,key="max news slider 2")
    freshness=st.selectbox("Select news Freshness ['Day', 'Week','Month'] ",['Day', 'Week','Month'],key="freshnewss news slider 2")
    sort_by=st.selectbox("Sort By ['RelevanceRanking', 'Date'] ",["Relevance", 'Date'],key="sortby news slider 2")
    search_term =  st.text_input(label="Search News",placeholder="Search News",max_chars=100,key="search term news slider 2")
    if search_term: 
        if st.button("Click to Search News ",key="search button 2"):
            get_news_and_put_download_button("Bing News Search API",search_term,freshness,max_news,sort_by)

with tab3:
    use_function=st.selectbox("get['Top Headlines' OR 'Everything'] ",['Top Headlines', 'Everything'])
    pageSize = st.slider("Select pageSize",min_value=1,max_value=100,step=1,value=30)
    page=st.slider("Select page",min_value=1,max_value=10,step=1,value=1)
    search_term =  st.text_input(label="Search News",placeholder="Search News",max_chars=100,key="search term news slider 3")
    if use_function: 
        newsapi = NewsApi()
        if use_function == "Everything":
            from_date = st.date_input(label = "A date for the oldest article",format="YYYY-MM-DD",value=one_month_ago)
            to_date = st.date_input(label="A date for the newest article",format="YYYY-MM-DD")
            language = st.selectbox("select language",["ar","de","en","es","fr","he","it","nl","no","pt","ru","sv","ud","zh",])
            sort_by=st.selectbox("Sort By ['RelevanceRanking', 'Date'] ",["relevancy", 'popularity','publishedAt'])
            if search_term:
                if st.button("Click to Search News ",key="search button 3.1"):
                    all_news = newsapi.get_everything_in_news(search_term,from_date,to_date,language,sort_by,pageSize,page)
                    st.write(all_news)
        else:
            country = st.selectbox("select country",['us',"in"])
            category=st.selectbox("select the category",["business","entertainment","general","technology","health","science","sports"])
            if st.button("Click to Search News ",key="search button 3.2"):
                all_news = newsapi.get_top_headlines_news(search_term,country,category,pageSize,page)
                st.write(all_news)


with tab4:
    use_function=st.selectbox("get['Articles' OR 'Events'] ",['Articles', 'Events'])
    pageSize = st.slider("Select pageSize",min_value=1,max_value=100,step=1,value=30,key="pageSize tab4")
    page=st.slider("Select page",min_value=1,max_value=10,step=1,value=1,key="page tab4")    
    sort_by=st.selectbox("Sort By",["date", "rel", "sourceImportance", "sourceAlexaGlobalRank", "sourceAlexaCountryRank", "socialScore", "facebookShares"],key="sort_by tab4")
    articleBodyLen = -1
    from_date = st.date_input(label = "A date for the oldest article",format="YYYY-MM-DD",value=one_month_ago,key="from date tab4")
    to_date = st.date_input(label="A date for the newest article",format="YYYY-MM-DD",key="to date tab4")
    categoryUri = st.selectbox("select category as Business",[None, "news/Society","news/Business","news/Accounting","news/Politics","news/Arts","news/Arts and Entertainment","news/Technology","news/Sports","news/Health","news/Environment"])
    language = st.selectbox("select language",language_codes)

    if use_function:
        news_ai = NewsAiApi(language)
        if use_function == "Articles":
            keywords =  st.text_input(label="Use , to use multiple keyword search ",placeholder="Search News",max_chars=1000,key="keyword tab4")
            dataType = st.selectbox("Data Type ['news', 'press releases', 'blog'] ",["news", "pr", "blog"],key="data type tab4")
            resultType = st.selectbox("resultType",["articles", "uriWgtList", "langAggr", "timeAggr", "sourceAggr", "sourceExAggr", "authorAggr", "keywordAggr", "locAggr", "conceptAggr", "conceptGraph", "categoryAggr", "dateMentionAggr", "sentimentAggr", "recentActivityArticles"])
            keywords = keywords.split(",")
            if st.button("Click to Search News ",key="search button 4.1"):
                response = news_ai.getArticles(pageSize,page,sort_by,resultType,articleBodyLen,from_date,to_date,dataType,categoryUri,language,keywords)
                st.write(response)
        else:
            resultType = st.selectbox("resultType",["events", "uriWgtList", "timeAggr", "locAggr", "locTimeAggr", "sourceAggr", "authorAggr", "keywordAggr", "conceptAggr", "conceptGraph", "categoryAggr", "breakingEvents", "sentimentAggr", "dateMentionAggr", "recentActivityEvents"])
            if st.button("Click to Search News ",key="search button 4.2"):
                response = news_ai.getEvents(pageSize,page,sort_by,resultType,articleBodyLen,from_date,to_date,categoryUri,language)
                st.write(response)

