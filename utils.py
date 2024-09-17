import datetime,os,requests,json
import pandas as pd
import streamlit as st
import gnews
# from azure.cognitiveservices.search.newssearch import NewsSearchClient
# from msrest.authentication import CognitiveServicesCredentials
# client = NewsSearchClient()
# client.news.search
# search_term = "Quantum Computing"
from typing import List,Tuple
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts.prompt import PromptTemplate
from operator import itemgetter
# from langchain_core.output_parsers import StrOutputParser
import uuid
from constant import *
import tempfile
import random
import string
from newsapi import NewsApiClient



# def initialize_chatgpt_chain():
#     SUMMARIZE_TEXT_PROMPT = """Summarize the following news article. Make the summary as long as necessary to include all the relevant information.
#     "{text}"
#     SUMMARY:"""
#     CHAT_LLM = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'),model=os.getenv('OPENAI_MODEL'))
#     prompt = PromptTemplate.from_template(SUMMARIZE_TEXT_PROMPT)
#     summarize_chain =( itemgetter("text")
#     |prompt
#     | CHAT_LLM
#     |StrOutputParser())
#     return summarize_chain


class NewsApi():
    def __init__(self):
        self.newsapi = NewsApiClient(api_key=os.getenv('NEWSAPI_API_KEY'))
        

    # Init
    def get_everything_in_news(self,query,from_date,to_date,language,sortBy,pageSize,page):
        all_articles = self.newsapi.get_everything(q=query,language=language,from_param=from_date,to=to_date,sort_by=sortBy,page_size=pageSize,page=page)
        if all_articles["status"] == "ok":
            return all_articles
        else:
            print("all_articles response = ",all_articles)
            return all_articles
    
    def get_top_headlines_news(self,query,country,category,pageSize,page):
        all_articles = self.newsapi.get_top_headlines(q=query,country=country,category=category,page_size=pageSize,page=page)
        if all_articles["status"] == "ok":
            return all_articles
        else:
            print("all_articles response = ",all_articles)
            return all_articles
        
class NewsAiApi():
    def __init__(self,language):
        self.getArticles_end_point = "https://eventregistry.org/api/v1/article/getArticles"
        self.getEvent_end_point = "https://eventregistry.org/api/v1/event/getEvents"
        self.payload = {
            "apiKey": os.getenv('NEWS_AI_API_KEY'),
            "includeArticleConcepts": True,
        }
        
    def getArticles(self,pageSize,page,sort_by,resultType,articleBodyLen,from_date,to_date,dataType,categoryUri,language,keywords=None):
        

        self.payload.update({"articlesPage":page,
                             "articlesCount":pageSize,
                             "articlesSortBy":sort_by,
                             "resultType":resultType,
                             "articlesArticleBodyLen":articleBodyLen,
                             "dataType":dataType,
                             "lang":language
                             })
        if categoryUri:
            self.payload.update({"dateStart":from_date.strftime("%Y-%m-%d"),"dateEnd":to_date.strftime("%Y-%m-%d"),"categoryUri":categoryUri})
        else:
            self.payload.update({"dateStart":from_date.strftime("%Y-%m-%d"),"dateEnd":to_date.strftime("%Y-%m-%d")})
        if not(keywords == None or keywords =="" or keywords ==[] ):
            self.payload.update({"keyword":keywords})
        else:
            pass
        print(self.payload)
        response =  requests.get(self.getArticles_end_point,json=self.payload)
        if response.status_code == 200:
            return response.json()
        else :
            try:
                return response.json()
            except:
                return response.status_code
    
    def getEvents(self,pageSize,page,sort_by,resultType,articleBodyLen,from_date:datetime.date,to_date:datetime.date,categoryUri,language):
        self.payload.update({"eventsPage":page,
                             "eventsCount":pageSize,
                             "eventsSortBy":sort_by,
                             "resultType":resultType,
                             "articlesArticleBodyLen":articleBodyLen,
                             "lang":language

                             })
        if categoryUri:
            self.payload.update({"dateStart":from_date.strftime("%Y-%m-%d"),"dateEnd":to_date.strftime("%Y-%m-%d"),"categoryUri":categoryUri})
        else:
            self.payload.update({"dateStart":from_date.strftime("%Y-%m-%d"),"dateEnd":to_date.strftime("%Y-%m-%d")})
        print(self.payload)
        response =  requests.get(self.getEvent_end_point,json=self.payload)
        if response.status_code == 200:
            return response.json()
        else :
            try:
                return response.json()
            except:
                return response.status_code

class GNews():
    def __init__(self,targate,days:int,max_news:int,summarize) -> None:
        self.targate = targate
        
        self.days = days
        self.max_news=max_news
        self.summarize=summarize
        if summarize:
            # self.summarize_chain = initialize_chatgpt_chain()
            pass
        pass

    def _get_original_url(self,redirect_url):
        try:
            response = requests.get(redirect_url, allow_redirects=True)
            return response.url
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None


    def _update_news(self,gnews_obj:gnews.GNews,news:dict)->(dict):
        import newspaper
        article = gnews_obj.get_full_article(news['url'])
        title=news.get("title")
        news["source"]="GNews"
        news["id"] = uuid.uuid4().hex
        description=news.get("description")
        if article:
            if article.text =='':
                if article.meta_description and article.meta_description !="":
                    article.text = article.meta_description
                else:
                         article.title = title
                         article.text = "Unable to get the text "
                         article.images = None
                         article.authors =None
                        
            else:
                         article.title = title
                         article.text = "Unable to reach the website "
                         article.images = None
                         article.authors =None
                        

            news.update({"title": article.title ,
                        "text": article.text ,
                        "images": article.images ,
                        "authors": article.authors 
                        })
            news["url"] = self._get_original_url(news['url'])
            if self.summarize:
                summary_text = f"Title: {title}\n\nDiscription:{description}\n\nText:{article.text}"
                news["summary"] = self.summarize_chain.invoke({"text":summary_text})
            if news.get("images"):
                news["images"] = list(news.get("images"))
            else:
                news["images"] = list()
            return news
        else:
            print("install newspaper3k in your shell")
            return
    def _get_yy_mm_dd():
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day
        return year,month,day
    
    def write_list_of_gnews(self,list_of_news)->(None):
        length_of_news = len(list_of_news)
        st.write(f'RAW DATA of {length_of_news} Google News.....')
        with st.expander("See Raw Data"):
            st.write(list_of_news)
        for news in list_of_news:
            with st.container() :
                title=news.get("title")
                description=news.get("description")
                published_date= news.get("published date")
                url=news.get("url")
                publisher=news.get("publisher")
                text=news.get("text")
                image_urls=news.get("images")
                authors=news.get("authors")
                publisher_title= publisher.get("title")
                publisher_url= publisher.get("href")
                st.header('Title')
                st.write(title)
                st.write(f'URL:- {url}')
                st.subheader('Description')
                st.write(description)
                if self.summarize:
                        st.subheader('Summary')
                        summary = news["summary"]
                        st.write(f" {summary}")
                st.subheader('Text')
                if text:
                    st.write(f'Text:- {text[:20]}.....')
                    with st.expander("See Full Text"):
                        st.write(text)
                else:
                    st.write(f'Text:- Error(failed with 401 Client Error) Unable to extract Text')
                if image_urls and len(image_urls):
                    news["images"] = list(news.get("images"))
                    st.subheader(f'Images')
                    image_urls = list(image_urls)
                    
                    with st.expander("See Images"):
                        st.image(image_urls,width=200)
                else:
                    news["images"] = list()
                if authors:
                    col1, col2, col3 = st.columns(3)
                    col1.subheader(f"Publiser")
                    col1.write(f"Publisher Url= {publisher_url}")
                    col1.write(publisher_title)

                    col2.subheader(f"Authors ")
                    col2.write(','.join(authors))

                    col3.subheader(f"Published Date")
                    col3.write(published_date)
                else:
                    col1, col2 = st.columns(2)
                    col1.subheader(f"Publiser ")
                    col1.write(f"Publisher Url= {publisher_url}")
                    col1.write(publisher_title)

                    col2.subheader(f"Published Date")
                    col2.write(published_date)
                st.write("--------------------------------------------\n\n")

    
    def get_news(self)->(List[dict]):
        news = gnews.GNews()
        # news.get_news_by_topic(topic="BUSINESS")
        news.period = (self.days)  # News from last 7 days
        news.max_results = self.max_news  # number of responses across a keyword
        news.country = 'India'  # News from a specific country 
        news.language = 'english'  # News in a specific language
        # news.exclude_websites = ['yahoo.com', 'cnn.com']  # Exclude news from specific website i.e Yahoo.com and CNN.com
        # year,month,day = get_yy_mm_dd()
        # news.start_date = (year, month, day) # Search from (present date, present month, present year)
        # news.end_date = (year, month, day-days) # Search until (present day-7days, present month, present year)
        news_response = news.get_news(f"{self.targate}")
        list_of_news = list(map(lambda x :self._update_news(gnews_obj=news,news=x),news_response))    
        list_of_news = [news_item for news_item in list_of_news if news_item is not None]
        return list_of_news
    
    def get_and_wright(self):
        list_of_news = self.get_news()
        self.write_list_of_gnews(list_of_news=list_of_news)


class BingNews():
    def __init__(self,targate,freshness,max_news,sort_by,summarize) -> None:
        self.azure_subscription_key=os.getenv('AZURE-SUBSCRIPTION-KEY')
        self.azure_end_point=os.getenv('AZURE-ENDPOINT')
        self.freshness = freshness
        self.max_news=max_news
        self.sort_by=sort_by
        self.targate = targate
        self.summarize=summarize
        if summarize:
            # self.summarize_chain = initialize_chatgpt_chain()
            pass

    def _update_news(self,news:dict)->(dict):
        title=news.get("name")
        description=news.get("description")
        news["source"]="Bing"
        news["id"] = uuid.uuid4().hex
        gnews_obj = gnews.GNews()
        article = gnews_obj.get_full_article(news['url'])
        if article:
            if article.text =='':
                if article.meta_description and article.meta_description !="":
                    article.text = article.meta_description
                else:
                    article.text = "Unable to get full context of the article"
            news.update({
                "title":title,
                "text": article.text ,
                "authors": article.authors 
                            })
        else:
            return news.update({
                "title":news["title"] if news.get("title") else"Unable to reach URL through newspaper3k Article()",
                "text": "Unable to reach URL through newspaper3k Article()" ,
                "authors": "unable to get data" 
                            })
        if self.summarize:
            summary_text = f"Title: {title}\n\nDiscription:{description}"
            news["summary"] = self.summarize_chain.invoke({"text":summary_text})
        
        return news
    def get_news(self):
        search_term = f"{self.targate}"
        headers = {"Ocp-Apim-Subscription-Key" : self.azure_subscription_key}
        params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML","freshness":self.freshness,"count":self.max_news,"sortBy":self.sort_by,"mkt":"en-IN"}
        response = requests.get(self.azure_end_point, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        list_of_news = list(map(self._update_news, search_results["value"]))
        list_of_news = [news_item for news_item in list_of_news if news_item is not None]
        return list_of_news

    def get_time(self,time_stamp:str):
        datetime_without_milliseconds = time_stamp[:23]
        now = datetime.datetime.now()
        # Parse the string into a datetime object
        dt = datetime.datetime.fromisoformat(datetime_without_milliseconds)

        # Access different parts of the datetime object
        year = now.year - dt.year
        month = now.month -dt.month
        day = now.day -dt.day
        hour = now.hour -dt.hour
        minute = now.minute -dt.minute
        second = now.second -dt.second

        # Print the datetime object (including timezone information)

        # You can also format the datetime object into a different string format
        formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        # Accessing the difference components
        date_dcit = {
        "year" : year,
        "month" : month,
        "days" : day,
        "hours" : hour,
        "minute" : minute,
        "seconds" : second
        }
        time = f"{date_dcit['year']} Y" if date_dcit['year']  != 0 else f"{date_dcit['month']} M" if date_dcit['month']  != 0 else f"{date_dcit['days']} D" if date_dcit['days']  != 0 else f"{date_dcit['hours']} H" if date_dcit['hours']  != 0 else f"{date_dcit['minute']} M" if date_dcit['minute']  != 0 else f"{date_dcit['seconds']} S"
        return time
    

    def write_list_of_bing_news(self,list_of_news)->(None):
        st.markdown("""
            <style>
            .discription-font {
                font-size:17px !important;
                font-weight:light !important;
                padding-left: 50px;
            }
            .title-font {
                font-size:25px !important;
                font-weight:bold !important;
            }
            </style>
            """, unsafe_allow_html=True)
        length_of_news = len(list_of_news)
        st.write(f'RAW DATA of {length_of_news} Bing News.....')
        with st.expander("See Raw Data"):
            st.write(list_of_news)
        for news in list_of_news:
            with st.container() :
                published_date= news.get("datePublished")
                st.write(self.get_time(published_date))
                col1, col2 = st.columns([0.7,0.3])
                url=news.get("url")
                providers=news.get("provider")
                image=news.get("image")
                category=news.get("category")
                title=news.get("name")
                text=news.get("text")
                description=news.get("description")
                with col1:
                    st.write(f'<h5 class ="title-font">{title}</h5>',unsafe_allow_html=True)
                    st.write(f'<p class ="discription-font">{description}</p>',unsafe_allow_html=True)
                with col2:
                    if image:
                        image_url = image["thumbnail"]["contentUrl"]
                        st.image(image_url,width=200)
                st.write(f'URL:- {url}')
                if self.summarize:
                        st.subheader('Summary')
                        summary = news["summary"]
                        st.write(f"{summary}")
                if text:
                    st.write(f'Text:- {text[:20]}.....')
                    with st.expander("See Full Text"):
                        st.write(text)
                
                if providers:
                    table_data = []
                    for provider in providers:
                        table_row = []
                        table_row.append(provider['_type'])
                        table_row.append(provider['name'])
                        if provider.get('image'):
                            table_row.append(provider['image']['thumbnail']["contentUrl"])
                        else:
                            table_row.append(None)
                        table_data.append(table_row)
                    df = pd.DataFrame(table_data, columns=("type","name","image"))
                    col1, col2, col3 = st.columns(3)
                    col1.subheader(f"Provide ")
                    col1.table(df)

                    col2.subheader(f"Published Date")
                    col2.write(published_date)

                    col3.subheader(f"Category")
                    col3.write(category)
                    
                st.write("--------------------------------------------\n\n")
        
    
    def get_and_wright(self):
        list_of_news = self.get_news()
        self.write_list_of_bing_news(list_of_news=list_of_news)

def get_download_json_str(list_of_news,source):
    op_news_list = []
    for news in list_of_news:
        if source=="Bing":
            provider_name = news['provider'][0]['name'] if news.get("provider") else None
        elif source=="GNews":
            provider_name = news['publisher']["title"] if news.get("publisher") else None
        else :
            provider_name=None
        dict = {
            "type": "news",
            "source": source,
            "sourceUrl": news.get('url'),
            "company": {
                "name": "string",
                "website": "string",
                "industry": "string",
                "employeeCount": "number"
            },
            "summary":news.get("summary"),
            "content": news.get("text"),
            "title":news.get("title"),
            "description":news.get("description"),
            "datePublished": news.get("datePublished"),
            "author": news.get("authors"),
            "metadata": {
                "news": {
                "publication": provider_name,
                "category": news.get("category")
                },}
        }
        op_news_list.append(dict)

    json_string = json.dumps(op_news_list)
    return json_string

def get_op_news_list(list_of_news):
    op_news_list = []
    for news in list_of_news:
        if news["source"]=="Bing":
            provider_name = news['provider'][0]['name'] if news.get("provider") else None
        elif news["source"]=="Google":
            provider_name = news['publisher']["title"] if news.get("publisher") else None
        else :
            provider_name=None
        dict = {
            "id":news["id"],
            "type": "news",
            "source": news["source"],
            "sourceUrl": news.get('url'),
            "company": {
                "name": "string",
                "website": "string",
                "industry": "string",
                "employeeCount": "number"
            },
            "summary":news.get("summary"),
            "content": news.get("text"),
            "title":news.get("title"),
            "description":news.get("description"),
            "datePublished": news.get("datePublished"),
            "author": news.get("authors"),
            "metadata": {
                "news": {
                "publication": provider_name,
                "category": news.get("category")
                },}
        }
        op_news_list.append(dict)
    return op_news_list

def filter_by_urls(news:dict,urls_entries:set):
    if news["sourceUrl"] not in urls_entries:
        urls_entries.add(news["sourceUrl"])
        return news
    else:
        return


def write_news_for_bing_and_google(list_of_news) -> None:
    google = GNews(targate="",days=1,max_news=1,summarize=False)
    bing_news = BingNews("","","","",False)
    bing_list = list(filter(lambda x:x["source"]=="Bing",list_of_news))
    google_list=list(filter(lambda x:x["source"]=="GNews",list_of_news))
    bing_news.write_list_of_bing_news(bing_list)
    google.write_list_of_gnews(google_list)
    return None

def get_datetime_stamp():
    # Get the current date and time
    current_datetime = datetime.datetime.now()
    
    # Format the datetime object as "DD-MM-YYYY hh:mm:ss"
    datetime_stamp = current_datetime.strftime('%d-%m-%Y_%H:%M:%S')
    
    return datetime_stamp
def create_file_with_parents(file_path):
    # Create a Path object
    file = Path(file_path)
    
    # Create parent directories if they don't exist
    file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create the file
    file.touch()
def split_list(input_list, split_length):
    return [input_list[i:i+split_length] for i in range(0, len(input_list), split_length)]
def _random_str(length):
    
    return ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=length))

@st.cache_data
def get_news(news_choice,targates,freshness,max_news,summarize=True,sort_by="Relevance")->(Tuple[List[dict],bool,str]):
    list_of_targate_output = []
    for targate in targates:
        time_stape = get_datetime_stamp()
        today_date = time_stape.split("_")[0]
        targate_folder_name = targate.replace(' ', '_')
        files_dir = os.path.join(TEMP_BASE_JSON_DIR,time_stape,targate_folder_name)
        list_of_news=[]
        output=False
        match news_choice:
            case 'GNews':
                if targate and freshness:
                    with st.status(f"Getting News for {targate}..."):
                        days = FRESHNESS_DICT.get(freshness)
                        gnews = GNews(targate=targate,days=days,max_news=max_news,summarize=summarize)
                        st.write("Getting news from Google...")
                        list_of_news = gnews.get_news()
                        output = True
                else:
                    st.subheader("Please Enter Company name and NO of days")
            case 'Bing News Search API':
                if targate and freshness and sort_by:
                    with st.status(f"Getting News {targate}..."):
                        bing_news = BingNews(targate=targate,freshness=freshness,max_news=max_news,sort_by=sort_by,summarize=summarize)
                        st.write("Getting news from Bing...")
                        list_of_news = bing_news.get_news()
                        output = True

                else:
                    st.subheader("Please Enter Company name and Freshness")
            case "Google + Bing":
                if targate and freshness and sort_by:
                    with st.status(f"Getting News for {targate}..."):
                        days = FRESHNESS_DICT.get(freshness)
                        st.write("Getting news from Google...")
                        gnews = GNews(targate=targate,days=days,max_news=max_news,summarize=summarize)
                        gnews_list_of_news = gnews.get_news()
                        st.write("Getting news from Bing...")
                        bing_news = BingNews(targate=targate,freshness=freshness,max_news=max_news,sort_by=sort_by,summarize=summarize)
                        bing_list_of_news = bing_news.get_news()
                        st.write("Almost Done ...")

                        list_of_news.extend(gnews_list_of_news)
                        list_of_news.extend(bing_list_of_news)
                    
                    output=True
                else:
                    st.subheader("Please Enter Company name and Freshness")
            case _:
                st.subheader("Yet to implement")

        url_entries = set()
        json_news_data = get_op_news_list(list_of_news)
        json_news_data = list(filter(lambda x: filter_by_urls(x,url_entries),json_news_data))
        newsted_list_news_json_data = split_list(input_list=json_news_data,split_length=8)
        for lst_news_json in newsted_list_news_json_data:
            file_name = f'{targate_folder_name}_{_random_str(5)}__{time_stape}.json'
            TEMP_NEWS_JSON_FILE_LOCATION = os.path.join(files_dir,file_name)
            create_file_with_parents(TEMP_NEWS_JSON_FILE_LOCATION)
            json_string = json.dumps(lst_news_json)
            with open(TEMP_NEWS_JSON_FILE_LOCATION,"w+") as file:
                file.write(json_string)
        list_of_targate_output.append({
            "targate": targate,
            "list_of_news":list_of_news,
            "output":output,
            "files_dir":files_dir
        })
    return list_of_targate_output

def initialize_session():
    sort_by_choice = st.session_state.get(SESSION_SORT_NEWS_BY_KEY)

    if not sort_by_choice:
        st.session_state[SESSION_SORT_NEWS_BY_KEY] = "Relevance"

def read_analyzed_report(report_path)->(str):
    print(report_path,"<##########report_path")
    report_path = os.path.join(READ_REPORT_BASE_DIR,report_path)
    with open(report_path, 'r') as file:
        return file.read()
        
def get_tab_dict_for_news_view(targate_list):
    # Create variables dynamically in the global namespace
    op_tabs_dict ={}
    for i in range(len(targate_list)):
        op_tabs_dict.update({f'var{i}':st.tabs([targate_list[i]])})
    return op_tabs_dict

def update_report(x,obj):
    x.update({"targate":obj["targate"]})
    return x


def get_news_and_put_download_button(news_choice,search_terms:str,freshness,max_news,sort_by):
    search_terms = search_terms.split(",")
    list_of_targate_output = get_news(news_choice,search_terms,freshness,max_news,False,sort_by)
    # print("list_of_targate_output",list_of_targate_output,"list_of_targate_output")
    for targate_output in list_of_targate_output:
        targate=targate_output.get("targate")
        list_of_news=targate_output.get("list_of_news")
        output=targate_output.get("output")
        files_dir=targate_output.get("files_dir")
        print("list_of_news >>>>>>>>>>>>>>>",list_of_news)
        if output ==True:
            url_entries = set()
            json_news_data = list_of_news
            # json_news_data = get_op_news_list(list_of_news)
            # json_news_data = list(filter(lambda x: filter_by_urls(x,url_entries),json_news_data))
            json_string = json.dumps(json_news_data)
            write_news_for_bing_and_google(json_news_data)
            with st.sidebar:
                st.download_button(
                            label=f"Download {targate} {news_choice} JSON",
                            file_name="data.json",
                            mime="application/json",
                            data=json_string,
                        )
        else:
            st.subheader("Unable to genrate Output news")