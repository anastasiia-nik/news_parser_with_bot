from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime

from news.models import News


class NewsParser(ABC):

    @abstractmethod
    def last_news(self) -> list[News]:
        '''
        n = News()
        n.save()
        '''


@dataclass
class NewsExternal():
    news_title: str
    news_author: str
    news_data: datetime
    news_text: str
    news_photo: str
    news_tags: [str]
