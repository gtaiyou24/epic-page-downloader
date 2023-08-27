from di import DIContainer
from fastapi import APIRouter

from application.page import PageApplicationService
from port.adapter.resource.page.response import DownloadedPageJson

router = APIRouter(
    prefix='/pages',
    tags=['ページ系']
)


@router.get('/download',
            response_model=DownloadedPageJson,
            name='ページダウンロード機能',
            description='HTMLをダウンロードします')
def download(url: str, device: str = 'SP') -> DownloadedPageJson:
    page_application_service = DIContainer.instance().resolve(PageApplicationService)
    dpo = page_application_service.download(url, device)
    return DownloadedPageJson.of(dpo)
