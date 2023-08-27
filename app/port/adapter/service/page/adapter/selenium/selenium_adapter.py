from typing import Optional

import requests
from selenium.common import JavascriptException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from domain.model.page import Page, HttpStatus
from domain.model.page.html import HTML, CharacterCode
from domain.model.url import URL
from domain.model.user_agent import UserAgent
from exception import SystemException, ErrorCode
from port.adapter.service.page.adapter import PageAdapter
from port.adapter.service.page.adapter.selenium import ChromeBuilder


class SeleniumAdapter(PageAdapter):
    def __init__(self):
        self.__builder = ChromeBuilder()

    def download(self, url: URL, user_agent: UserAgent) -> Page:
        with self.__builder.user_agent(user_agent).build() as web_driver:
            try:
                web_driver.implicitly_wait(10)
                web_driver.get(url.value)
                response = requests.get(web_driver.current_url,
                                        headers={'User-Agent': user_agent.value},
                                        timeout=(10.0, 20.0))
            except TimeoutException:
                raise SystemException(ErrorCode.PAGE_TIMEOUT, 'page {} timeout.'.format(url.value))

            # 最下部までスクロールする
            self.__scroll_to_bottom(web_driver)

            # ページの読み込みが完了するまで待機する
            WebDriverWait(web_driver, 10)\
                .until(expected_conditions.presence_of_all_elements_located)

            return Page(
                URL(web_driver.current_url),
                HttpStatus.value_of(response.status_code),
                HTML(web_driver.page_source, CharacterCode.value_of(response.apparent_encoding))
            )

    @staticmethod
    def __scroll_to_bottom(web_driver) -> None:
        try:
            web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except JavascriptException as e:
            # NOTE: 上記の方法でスクロールできない場合
            web_driver.find_element(By.TAG_NAME, "body").click()
            web_driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)