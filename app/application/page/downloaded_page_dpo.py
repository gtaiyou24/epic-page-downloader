from dataclasses import dataclass

from domain.model.page import Page


@dataclass(unsafe_hash=True, frozen=True)
class DownloadedPageDpo:
    page: Page

    def page_is_downloaded(self) -> bool:
        return self.page.is_ok()
