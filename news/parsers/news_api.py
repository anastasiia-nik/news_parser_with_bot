import requests

from base import NewsParser
from bs4 import BeautifulSoup

BASE_URL = 'https://www.pravda.com.ua/news/'




class Upravda(NewsParser):

    @staticmethod
    def collect_all_news() -> list[str]:
        resp = requests.get(BASE_URL)
        bs = BeautifulSoup(resp.text, 'lxml')
        news_on_page = bs.find_all('div', class_='article_news_list')
        news_list = []
        for news in news_on_page:
            temp_link = news.find('a').attrs['href']
            if 'https' not in temp_link:
                news_list.append('https://www.pravda.com.ua/' + temp_link)
        return news_list

    @staticmethod
    def parse(link):
        title - h1
        author - post_author.text
        data - post time
        photo post_photo_news_img scr





test = Upravda()
test.parse_all_news()
