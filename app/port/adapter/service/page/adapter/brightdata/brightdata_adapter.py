import os

import requests
from selenium.common import TimeoutException, JavascriptException
from selenium.webdriver import Remote, ChromeOptions, Keys
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By

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

    def download(self, url: URL, user_agent: UserAgent) -> Page:
        self.__options.add_argument(f'--user-agent={user_agent.value}')
        with Remote(self.__remote_connection, options=self.__options) as web_driver:
            try:
                web_driver.get(url.value)

                try:
                    web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except JavascriptException as e:
                    # NOTE: 上記の方法でスクロールできない場合
                    web_driver.find_element(By.TAG_NAME, "body").click()
                    web_driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

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