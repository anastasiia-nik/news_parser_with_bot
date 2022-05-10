import json
from concurrent.futures import ThreadPoolExecutor, as_completed
# from time import strptime, strftime
from datetime import datetime

import requests

# from base import NewsParser
from bs4 import BeautifulSoup

from news.models import News
from news.parsers.base import NewsExternal


class Upravda():
    BASE_URL = 'https://www.pravda.com.ua/news/'

    def __init__(self):
        self.list_all_news_links = []
        self.all_news = []

    # @staticmethod
    def collect_all_news(self):
        resp = requests.get(self.BASE_URL)
        bs = BeautifulSoup(resp.text, 'lxml')
        news_on_page = bs.find_all('div', class_='article_news_list')
        news_list = []
        for news in news_on_page:
            temp_link = news.find('a').attrs['href']
            if 'http' not in temp_link:
                news_list.append('https://www.pravda.com.ua' + temp_link)
        self.list_all_news_links = self.filter_duplicate_links(news_list)


    def filter_duplicate_links(self, link_list):
        temp_list = []
        for link in link_list:
            if News.objects.filter(link=link).exists():
                continue
            temp_list.append(link)
        return temp_list


    def convert_data(self, data: str):
        dict_month = {'січня': 1,
                      'лютого': 2,
                      'березня': 3,
                      'квітня': 4,
                      'травня': 5,
                      'червня': 6,
                      'липня': 7,
                      'серпня': 8,
                      'вересня': 9,
                      'жовтня': 10,
                      'листопада': 11,
                      'грудня': 12,
                      }
        str_l = data.split()
        str_n = str_l[1] + '.' + str(dict_month[str_l[2]]) + '.' + str_l[3].strip(',') + ' ' + str_l[4]
        valid_data = datetime.strptime(str_n, '%d.%m.%Y %H:%M')
        return valid_data

    # @staticmethod
    def parse_one(self, link):

        news_info = {}
        # title - h1
        # author - post_author.text
        # data - post time
        # photo post_photo_news_img scr
        # tags - post_tags_item
        resp = requests.get(link)
        bs = BeautifulSoup(resp.text, 'lxml')
        news_title = bs.find('h1').text
        try:
            news_author = bs.find('span', class_='post_author').text.strip(' — ')
        except AttributeError:
            news_author = 'Anonimus'
            print(link)
        news_data = self.convert_data(bs.find('div', class_='post_time').text.split(' — ')[-1])
        news_text = bs.find('div', class_='post_text').text
        try:
            news_photo = bs.find('img', class_='post_photo_news_img').attrs['src']
        except:
            news_photo = ''
        news_tags_set = bs.find_all('span', class_='post_tags_item')
        news_tags = []
        for tag in news_tags_set:
            news_tags.append(tag.text)
        one_news = NewsExternal(news_title=news_title,
                                news_author=news_author,
                                news_data=news_data,
                                news_text=news_text,
                                news_photo=news_photo,
                                news_tags=news_tags,
                                news_link=link)
        # print(one_news)
        # self.all_news.append(one_news)
        # print(self.all_news[-1])
        return one_news

    def parse_all(self):
        self.collect_all_news()
        if self.list_all_news_links:
            self.all_news = self.grabber(self.list_all_news_links, self.parse_one)


        # for link in self.list_all_news_links:
        #     self.parse_one(link=link)
        # self.parse_one(self.list_all_news_links[0])


    # # temp = Upravda()
    # # temp.collect_all_news()
    # # temp.parse_all()
    #
    # # print(temp.all_news[0].news_data)
    # # str_d = 'Четвер, 5 травня 2022, 00:39'
    # dict_month = {'січеня':1,
    #               'лютого':2,
    #               'березня':3,
    #               'квітня':4,
    #               'травня':5,
    #               'червня':6,
    #               'липня':7,
    #               'серпня':8,
    #               'вересня':9,
    #               'жовтня':10,
    #               'листопада':11,
    #               'грудня':12,
    #               }
    #
    # str_l = str_d.split()
    # str_n = str_l[1]+'.'+str(dict_month[str_l[2]])+'.'+str_l[3].strip(',')+' '+str_l[4]
    #
    # str_true = '5.05.2020 12:12'
    #
    # data = datetime.strptime(str_n,'%d.%m.%Y %H:%M')
    # # data = strptime(str_true,'%d.%m.%Y %H:%M')
    #
    # print(data)

    def grabber(self, links: list, parser):
        with ThreadPoolExecutor(10) as executor:
            elements = []
            threads = []
            for page in links:
                threads.append(executor.submit(parser, page))
            for page in as_completed(threads):
                # print(page.result())
                elements.append(page.result())
        # print(elements)
        return elements
        # self.all_news = elements

    def to_json(self):
        general_list = []
        for item in self.all_news:
            general_list.append(item.__dict__)
        with open('news_test.json', 'w') as file:
            json.dump(general_list, file, indent=4, ensure_ascii=False, default=str)

# temp = Upravda()
# temp.collect_all_news()
#
# # print(temp.list_all_news_links)
#
# temp.parse_all()
# temp.to_json()
# # print(temp.all_news)
#
# print(len(temp.list_all_news_links))
# print(len(temp.all_news))
# print(temp.all_news[-1])
