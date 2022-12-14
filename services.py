import base64
import csv
import logging
import os
from glob import glob
from typing import Type, Union
from uuid import uuid4

from fastapi import HTTPException

from database import db_table
from models import CVFullRead, CVInsertIntoDB, CVShortRead, CVUpdate

__all__ = (
    'model_to_csv',
    'csv_to_model',
    'get_uuid',
    'clear_csv',
    'b64_to_file',
    'update_item_attrs',
    'update_encoded_string',
    'check_for_404',
    'check_for_404_with_item',
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
    with open('temp.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            cv_dict.update({row[0]: row[1]})

    # Model choice
    model = response_class(**cv_dict)
    return model


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())


def clear_csv() -> None:
    """Deletes all local .csv"""
    # Taking filenames
    removing_files = glob('./*.csv')

    # Removing files
    for i in removing_files:
        os.remove(i)

    # Logging the action
    logging.info("ALL LOCAL .csv ARE CLEARED SUCCESSFULLY!")


def b64_to_file(b64_str: bytes, title: str = 'temp.csv') -> None:
    """"Writes local .csv file from base64 string"""
    # Decoding base64
    image_64_decode = base64.b64decode(b64_str)

    # Creates a writable image and writes the decoded result
    image_result = open(title, 'wb')
    image_result.write(image_64_decode)


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
    response = db_table.update_item(
        Key={'cv_id': cv_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return response


def update_encoded_string(cv_id: str, encoded_string: bytes):
    """Updates single attr (encoded_string)"""
    # Querying the update to DynamoDB
    response = db_table.update_item(
        Key={'cv_id': cv_id},
        UpdateExpression=f'set cv_in_bytes = :cv_in_bytes',
        ExpressionAttributeValues={':cv_in_bytes': encoded_string}
    )
    return response


def check_for_404(container, message: str = "Item can't be found!"):
    """Checks container for 'empty' case"""
    if len(container) == 0:
        raise HTTPException(
            status_code=404,
            detail=message
        )


def check_for_404_with_item(container, item, message: str = "Item can't be found!"):
    """
    Checks response for 'empty' case
    Used only for checking responses of .get_item() function
    """
    if item not in container:
        raise HTTPException(
            status_code=404,
            detail=message
        )
