import requests

from domain.model.page import Page, HttpStatus
from domain.model.page.html import HTML, CharacterCode
from domain.model.url import URL
from domain.model.user_agent import UserAgent
from port.adapter.service.page.adapter import PageAdapter


class RequestsAdapter(PageAdapter):
    def download(self, url: URL, user_agent: UserAgent) -> Page:
        res = requests.get(url.value, headers={'User-Agent': user_agent.value}, timeout=(10.0, 20.0))
        return Page(
            URL(res.url),
            HttpStatus.value_of(res.status_code),
            HTML(
                res.text,
                CharacterCode.value_of(res.apparent_encoding)
            )
        )
