import boto3

from core.config import (AWS_ACCESS_KEY, AWS_REGION, AWS_SECRET_ACCESS_KEY,
                    DYNAMODB_ENDPOINT)

__all__ = (
    'cv_table',
    'company_table',
    'manager_table',
    'vacancy_table',
)


# Resource
dynamo_resource = boto3.resource("dynamodb", endpoint_url=DYNAMODB_ENDPOINT, aws_access_key_id=AWS_ACCESS_KEY,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

# Tables
cv_table = dynamo_resource.Table('cv_table')
company_table = dynamo_resource.Table('company_table')
manager_table = dynamo_resource.Table('manager_table')
vacancy_table = dynamo_resource.Table('vacancy_table')
