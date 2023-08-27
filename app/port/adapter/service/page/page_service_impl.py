from injector import inject

from domain.model.page import PageService, Page
from domain.model.url import URL
from domain.model.user_agent import UserAgent
from port.adapter.service.page.adapter import PageAdapter


class PageServiceImpl(PageService):
    @inject
    def __init__(self, page_adapter: PageAdapter):
        self.__page_adapter = page_adapter

    def download(self, url: URL, user_agent: UserAgent) -> Page:
        return self.__page_adapter.download(url, user_agent)
