from dotenv import dotenv_values
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

__all__ = (
    'AUTH_KEY',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'POSTGRES_DB',
    'POSTGRES_HOST',
    'TOKEN_MINUTES_TO_LIVE',
)

# Env variables
config = dotenv_values(".env")
if not config:
    config = dotenv_values("src/.env")


AUTH_KEY = config["AUTH_KEY"]
POSTGRES_USER = config["POSTGRES_USER"]
POSTGRES_PASSWORD = config["POSTGRES_PASSWORD"]
POSTGRES_DB = config["POSTGRES_DB"]
POSTGRES_HOST = config["POSTGRES_HOST"]
TOKEN_MINUTES_TO_LIVE = int(config["TOKEN_MINUTES_TO_LIVE"])


class Settings(BaseModel):
    authjwt_secret_key: str = AUTH_KEY
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return Settings()
