import abc

from domain.model.user_agent import UserAgent
from domain.model.page import Page
from domain.model.url import URL


class PageService(abc.ABC):
    @abc.abstractmethod
    def download(self, url: URL, user_agent: UserAgent) -> Page:
        pass
