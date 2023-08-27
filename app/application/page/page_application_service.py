import time

import requests
from injector import singleton, inject

from application.page import DownloadedPageDpo
from domain.model.page.html import HTML, CharacterCode
from domain.model.user_agent import UserAgent
from domain.model.user_agent.device import Device
from domain.model.page import PageService, Page, HttpStatus
from domain.model.url import URL


@singleton
class PageApplicationService:
    @inject
    def __init__(self, page_service: PageService):
        self.__page_service = page_service

    def download(self, an_url: str, a_device: str) -> DownloadedPageDpo:
        url = URL(an_url)
        device = Device.value_of(a_device)
        user_agent = UserAgent.random(device)

        response: requests.Response = requests.get(url.value, headers={'User-Agent': user_agent.value}, timeout=(10.0, 20.0))

        if response.ok:
            page = Page(
                URL(response.url),
                HttpStatus.value_of(response.status_code),
                HTML(response.text, CharacterCode.value_of(response.apparent_encoding))
            )
        else:
            time.sleep(1.5)
            page = self.__page_service.download(url, user_agent)

        return DownloadedPageDpo(page)
