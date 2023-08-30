from dotenv import dotenv_values

__all__ = (
    'DYNAMODB_ENDPOINT',
    'AWS_ACCESS_KEY',
    'AWS_SECRET_ACCESS_KEY',
    'AWS_REGION',
    'AUTH_KEY',
)

# Env variables
config = dotenv_values("src/.env")
DYNAMODB_ENDPOINT = config["DYNAMODB_ENDPOINT"]
AWS_ACCESS_KEY = config["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = config["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = config["AWS_REGION"]
AUTH_KEY = config["AUTH_KEY"]
