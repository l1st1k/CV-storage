import base64
import csv
import logging
import os
from glob import glob
from typing import Type, Union

from fastapi import HTTPException

from modules.company.models import CompanyInsertAndFullRead
from modules.company.services import get_company_by_id

from modules.cv.models import CVFullRead, CVInsertIntoDB, CVShortRead, CVUpdate, CVsFullRead

__all__ = (
    'model_to_csv',
    'csv_to_model',
    'clear_csv',
    'b64_to_file',
    'update_item_attrs',
    'update_encoded_string',
    'add_cv_to_company_model',
    'delete_cv_from_company_model',
    'delete_cv_from_db',
    'select_companys_cvs',
)


#  Settings
logging.basicConfig(level=logging.INFO)


def model_to_csv(model: CVFullRead) -> None:
    """Writes local .csv file from model"""
    cv_dict = dict(model)
    title = model.last_name + '.csv'
    with open(title, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(cv_dict.items())


def csv_to_model(
        response_class: Union[Type[CVFullRead], Type[CVShortRead], Type[CVInsertIntoDB]]
) -> Union[CVFullRead, CVShortRead, CVInsertIntoDB]:
    """Turns .csv into necessary model"""
    cv_dict = dict()
    with open('tmp/temp.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            cv_dict.update({row[0]: row[1]})

    # Model choice
    model = response_class(**cv_dict)
    return model


def clear_csv() -> None:
    """Deletes all local .csv"""
    # Taking filenames
    removing_files = glob('./tmp/*.csv')

    # Removing files
    for i in removing_files:
        os.remove(i)

    # Logging the action
    logging.info("ALL LOCAL .csv ARE CLEARED SUCCESSFULLY!")


def b64_to_file(b64_str: bytes, title: str = 'temp.csv') -> str:
    """"Writes local .csv file from base64 string"""
    # Decoding base64
    image_64_decode = base64.b64decode(b64_str)

    # Creates a writable image and writes the decoded result
    title = "tmp/" + title
    image_result = open(title, 'wb')
    image_result.write(image_64_decode)

    return title


def update_item_attrs(cv_id: str, model: CVUpdate):
    """Updates items attrs"""
    # Init expressions for DynamoDB update
    update_expression = "set"
    expression_attribute_values = {}
    attributes = model.dict()

    # Filling the expressions
    for key, value in attributes.items():
        if value:
            update_expression += f' {key} = :{key},'
            expression_attribute_values[f':{key}'] = value

    # Cutting the last comma
    update_expression = update_expression[:-1]

    # Querying the update to DynamoDB
    response = cv_table.update_item(
        Key={'cv_id': cv_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return response


def update_encoded_string(cv_id: str, encoded_string: bytes):
    """Updates single attr (encoded_string)"""
    # Querying the update to DynamoDB
    response = cv_table.update_item(
        Key={'cv_id': cv_id},
        UpdateExpression=f'set cv_in_bytes = :cv_in_bytes',
        ExpressionAttributeValues={':cv_in_bytes': encoded_string}
    )
    return response


def add_cv_to_company_model(company: CompanyInsertAndFullRead, cv: CVInsertIntoDB) -> None:
    # Querying the existing cvs
    existing_cvs = company.cvs if company.cvs else set()
    existing_cvs.add(cv.cv_id)  # Adding new cv_id

    # Update the cvs attribute in DynamoDB
    company_table.update_item(
        Key={'company_id': company.company_id},
        UpdateExpression="SET cvs = :cvs",
        ExpressionAttributeValues={
            ":cvs": existing_cvs
        }
    )


def delete_cv_from_company_model(company_id: str, cv_id: str) -> None:
    # Retrieve the company by ID
    company: CompanyInsertAndFullRead = get_company_by_id(company_id=company_id)

    # Check if the company exists and has a cvs attribute
    if company and company.cvs:
        # Remove the cv_id from the set of cvs
        if cv_id in company.cvs:
            company.cvs.remove(cv_id)
            # If set is empty - we set None
            company.cvs = None if not company.cvs else company.cvs

            # Update the cvs attribute in DynamoDB
            company_table.update_item(
                Key={'company_id': company.company_id},
                UpdateExpression="SET cvs = :cvs",
                ExpressionAttributeValues={
                    ":cvs": company.cvs
                }
            )


def delete_cv_from_db(cv_id: str) -> None:
    db_response = cv_table.delete_item(
            Key={
                'cv_id': cv_id
            }
        )

    # 404 validation
    if 'ConsumedCapacity' in db_response:
        raise HTTPException(
            status_code=404,
            detail='CV not found.'
        )


def select_companys_cvs(company_id: str) -> CVsFullRead:
    response = cv_table.scan(
        FilterExpression=Attr('company_id').eq(company_id)
    )
    items = response['Items']
    if items:
        return [CVFullRead(**document) for document in items]
    else:
        company = get_company_by_id(company_id=company_id)
        raise HTTPException(status_code=404, detail=f'There are no any cvs in {company.company_name}.')
