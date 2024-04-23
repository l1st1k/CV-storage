import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.datastructures import MutableHeaders

__all__ = ('configure_app_middlewares',)

logger = logging.getLogger(__name__)


class CustomRequest(Request):
    # TODO remove this bullshit =)))) (just a mock)

    def set_cookies_from_header(self):
        cookie_value = self.headers.get('cooookie')
        if cookie_value:
            # Assuming the value is a simple string; you may need to parse if it's formatted differently
            mutable_headers = MutableHeaders(raw=self.scope['headers'])
            for cookie in cookie_value.split(" "):
                mutable_headers.append('cookie', cookie)


def configure_app_middlewares(application: FastAPI) -> None:
    origins = [
        "http://localhost",
        "http://localhost:5173",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def cookie_logger(request, call_next):
        origin: str = request.headers.get('referer')
        same_port: bool = ":8000" in origin

        # IN-BOUND
        if same_port:
            logger.info(f"Request Cookies: {request.cookies}")
            response = await call_next(request)
        else:
            custom_request = CustomRequest(request.scope)
            custom_request.set_cookies_from_header()
            logger.info(f"Request Cookies: {custom_request.cookies}")
            response = await call_next(custom_request)

        # OUT-BOUND
        response_cookies = response.headers.getlist('set-cookie')
        logger.info(f"Response Cookies: {response_cookies}")
        if response_cookies and not same_port:
            response = JSONResponse(content={"cookies": response_cookies})

        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
