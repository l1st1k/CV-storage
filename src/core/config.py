from dotenv import dotenv_values

__all__ = (
    'DYNAMODB_ENDPOINT',
    'AWS_ACCESS_KEY',
    'AWS_SECRET_ACCESS_KEY',
    'AWS_REGION',
    'AUTH_KEY',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'POSTGRES_DB',
)

# Env variables
config = dotenv_values("src/.env")  # TODO remove local path
# config = dotenv_values(".env")

DYNAMODB_ENDPOINT = config["DYNAMODB_ENDPOINT"]
AWS_ACCESS_KEY = config["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = config["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = config["AWS_REGION"]
AUTH_KEY = config["AUTH_KEY"]
POSTGRES_USER = config["POSTGRES_USER"]
POSTGRES_PASSWORD = config["POSTGRES_PASSWORD"]
POSTGRES_DB = config["POSTGRES_DB"]
