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
        news_info = {}
        # title - h1
        # author - post_author.text
        # data - post time
        # photo post_photo_news_img scr
        # tags - post_tags_item
        resp = requests.get(link)
        bs = BeautifulSoup(resp.text, 'lxml')
        news_title = bs.find('h1')
        news_author = bs.find('div', class_='post_author').text
        news_data = bs.find('div', class_='post time').text
        news_photo = bs.find('div', class_='post_photo_news_img').find('img').attrs['scr']
        news_tags = bs.find_all('div', class_='post_tags_item').text










test = Upravda()
test.parse_all_news()
