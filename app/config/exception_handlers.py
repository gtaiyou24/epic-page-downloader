from fastapi import Request
from fastapi.responses import JSONResponse

from exception import SystemException


async def system_exception_handler(request: Request, exception: SystemException):
    exception.logging()
    return JSONResponse(
        status_code=exception.error_code.http_status,
        content={"message": exception.detail}
    )
