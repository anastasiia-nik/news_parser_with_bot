from abc import abstractmethod, ABC

from news.models import News


class NewsParser(ABC):

    @abstractmethod
    def last_news(self) -> list[News]:
        '''
        n = News()
        n.save()
        '''
