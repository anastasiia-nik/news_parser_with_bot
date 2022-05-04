from base import NewsParser
from bs4 import BeautifulSoup
from newsapi import NewsApiClient


#81941d1679c2475388fe5337be537783

# https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=81941d1679c2475388fe5337be537783



newsapi = NewsApiClient(api_key='81941d1679c2475388fe5337be537783')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

# /v2/top-headlines/sources
sources = newsapi.get_sources()

print(sources)



class Upravda(NewsParser):
    pass







