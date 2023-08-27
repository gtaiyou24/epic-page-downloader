from injector import singleton, inject

from application.page import DownloadedPageDpo
from domain.model.user_agent import UserAgent
from domain.model.user_agent.device import Device
from domain.model.page import PageService
from domain.model.url import URL


@singleton
class PageApplicationService:
    @inject
    def __init__(self, page_service: PageService):
        self.__page_service = page_service

    def download(self, an_url: str, a_device: str) -> DownloadedPageDpo:
        url = URL(an_url)

        device = Device.value_of(a_device)
        page = self.__page_service.download(url, UserAgent.random(device))

        return DownloadedPageDpo(page)
