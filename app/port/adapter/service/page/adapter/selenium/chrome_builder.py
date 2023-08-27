from __future__ import annotations

import atexit
import os
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService

from domain.model.user_agent import UserAgent


class ChromeBuilder:
    def __init__(self):
        self.__move_bin("headless-chromium")
        self.__move_bin("chromedriver")

        self.__options = webdriver.ChromeOptions()
        self.__options.binary_location = '/tmp/bin/headless-chromium'
        self.__options.add_argument("--headless")  # ヘッドレスモード
        self.__options.add_argument("--disable-gpu")  # 暫定的に必要なフラグ
        self.__options.add_argument('--lang=ja-JP')  # 日本語対応
        self.__options.add_argument("--ignore-certificate-errors")
        self.__options.add_argument("--disable-extensions")  # すべての拡張機能を無効にする
        self.__options.add_argument("--disable-dev-tools")
        self.__options.add_argument("--disable-dev-shm-usage")
        self.__options.add_argument("--no-zygote")
        self.__options.add_argument('--single-process')
        self.__options.add_argument("--no-sandbox")
        self.__options.add_argument("--disable-setuid-sandbox")
        self.__options.add_argument("--start-maximized")  # 最小画面で起動

    @staticmethod
    def __move_bin(fname, src_dir="/opt", dest_dir="/tmp/bin"):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        dest_file = os.path.join(dest_dir, fname)
        shutil.copy2(os.path.join(src_dir, fname), dest_file)
        os.chmod(dest_file, 0o775)

    @staticmethod
    def __remove_unnecessary_file():
        if os.path.exists('/tmp/bin/'):
            shutil.rmtree('/tmp/bin/')

    def user_agent(self, user_agent: UserAgent) -> ChromeBuilder:
        self.__options.add_argument(f'--user-agent={user_agent.value}')
        return self

    def build(self) -> webdriver.Chrome:
        driver = webdriver.Chrome(options=self.__options, service=ChromiumService(executable_path='/tmp/bin/chromedriver'))

        # web driverによるアクセスを検知し、拒否するサイトがあるので「navigator.webdriver=true」とならないようにする
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        atexit.register(driver.quit)
        atexit.register(self.__remove_unnecessary_file)
        return driver
