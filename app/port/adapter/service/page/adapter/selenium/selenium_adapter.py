from typing import Optional

from domain.model.page import Page
from domain.model.url import URL
from domain.model.user_agent import UserAgent
from port.adapter.service.page.adapter import PageAdapter


class SeleniumAdapter(PageAdapter):
    def download(self, url: URL, user_agent: UserAgent, wait: Optional[int]) -> Page:
        raise NotImplementedError()
