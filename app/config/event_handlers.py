from typing import NoReturn

from di import DIContainer, DI
from domain.model.page import PageService
from port.adapter.service.page import PageServiceImpl
from port.adapter.service.page.adapter import PageAdapter
from port.adapter.service.page.adapter.brightdata import BrightDataAdapter
from port.adapter.service.page.adapter.selenium import SeleniumAdapter


def startup_handler() -> NoReturn:
    for di in [DI.of(PageService, {}, PageServiceImpl),
               DI.of(PageAdapter, {'BrightData': BrightDataAdapter}, SeleniumAdapter)]:
        DIContainer.instance().register(di)


def shutdown_handler() -> NoReturn:
    pass
