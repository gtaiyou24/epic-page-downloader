from fastapi import FastAPI
from mangum import Mangum

from config import exception_handlers, event_handlers
from exception import SystemException
from port.adapter.resource.health import health_resource
from port.adapter.resource.page import page_resource

app = FastAPI(title='Epic Page Downloader')

app.add_exception_handler(SystemException, exception_handlers.system_exception_handler)

app.add_event_handler('startup', event_handlers.startup_handler)
app.add_event_handler('shutdown', event_handlers.shutdown_handler)

app.include_router(health_resource.router)
app.include_router(page_resource.router)


def handler(event, context):
    # Lambda起動時に初期処理を実行
    event_handlers.startup_handler()

    asgi_handler = Mangum(app, lifespan="off")
    return asgi_handler(event, context)
