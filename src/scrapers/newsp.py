import sys
import os

# Get the absolute path to the directory two levels above
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# Add this directory to the Python path
sys.path.append(two_levels_up)
import keys
NEWSAPI_KEY = "8338bcc886c64b0c8ba85323162fccb6"
import requests
import json
from newspaper import Article
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

def urlToArticle(url:str)-> Article:
    a = Article(url)
    a.download
    a.parse()
    return a

def browse_news_api(query:str, sortBy:str='publishedAt', language= None):
    all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

    len(all_articles)

if __name__ == "__main__":
    all_articles = newsapi.get_everything(q='Unfall AND Verkehr AND Schweiz',
                                      language='de',
                                      sort_by='relevancy',
                                      page=2)

    print(len(all_articles))

