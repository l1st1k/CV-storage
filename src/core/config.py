from dotenv import dotenv_values

__all__ = (
    'AUTH_KEY',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'POSTGRES_DB',
)

# Env variables
config = dotenv_values("src/.env")  # TODO remove local path
# config = dotenv_values(".env")


AUTH_KEY = config["AUTH_KEY"]
POSTGRES_USER = config["POSTGRES_USER"]
POSTGRES_PASSWORD = config["POSTGRES_PASSWORD"]
POSTGRES_DB = config["POSTGRES_DB"]
