import os

import requests
from selenium.common import TimeoutException
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

from domain.model.page import Page, HttpStatus
from domain.model.page.html import CharacterCode, HTML
from domain.model.url import URL
from domain.model.user_agent import UserAgent
from exception import SystemException, ErrorCode
from port.adapter.service.page.adapter import PageAdapter


class BrightDataAdapter(PageAdapter):
    def __init__(self):
        self.__remote_connection = ChromiumRemoteConnection(os.getenv('SELENIUM_REMOTE_SERVER'), 'goog', 'chrome')
        self.__options = ChromeOptions()
        self.__options.add_argument('--blink-settings=imagesEnabled=false')  # 画像を読み込まない
        # 通知を無効化
        self.__options.add_experimental_option('prefs', "'profile.default_content_setting_values.notifications': 2")

    def download(self, url: URL, user_agent: UserAgent) -> Page:
        self.__options.add_argument(f'--user-agent={user_agent.value}')
        with Remote(self.__remote_connection, options=self.__options) as web_driver:
            try:
                web_driver.get(url.value)
                response = requests.get(web_driver.current_url, headers={'User-Agent': user_agent.value})
            except TimeoutException:
                raise SystemException(ErrorCode.PAGE_TIMEOUT, 'page {} timeout.'.format(url.value))

            return Page(
                URL(web_driver.current_url),
                HttpStatus.value_of(response.status_code),
                HTML(
                    web_driver.page_source,
                    CharacterCode.value_of(response.apparent_encoding)
                )
            )