import boto3
from dotenv import dotenv_values

__all__ = (
    'cv_table',
    'company_table',
    'manager_table',
    'vacancy_table',
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

# Tables
cv_table = dynamo_resource.Table('cv_table')
company_table = dynamo_resource.Table('company_table')
manager_table = dynamo_resource.Table('manager_table')
vacancy_table = dynamo_resource.Table('vacancy_table')
