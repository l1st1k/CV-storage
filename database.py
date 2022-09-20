import boto3
from dotenv import dotenv_values

__all__ = (
    'db_table',
)

# Env variables
config = dotenv_values(".env")
DYNAMODB_ENDPOINT = config["DYNAMODB_ENDPOINT"]
AWS_ACCESS_KEY = config["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = config["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = config["AWS_REGION"]

# Resource
dynamo_resource = boto3.resource("dynamodb", endpoint_url=DYNAMODB_ENDPOINT, aws_access_key_id=AWS_ACCESS_KEY,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

# Table
db_table = dynamo_resource.Table('main_table')
