import base64
import csv
import logging
import os
from glob import glob
from typing import Type, Union
from uuid import uuid4

from database import db_table
from models import CVFullRead, CVInsertIntoDB, CVShortRead, CVUpdate

__all__ = (
    'model_to_csv',
    'csv_to_model',
    'get_uuid',
    'b64_to_local_csv',
    'clear_csv',
    'b64_to_file',
    'update_item_attrs'
)


#  Settings
logging.basicConfig(level=logging.INFO)


def model_to_csv(model) -> None:
    cv_dict = dict(model)
    with open('temp.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(cv_dict.items())


def csv_to_model(
        response_class: Union[Type[CVFullRead], Type[CVShortRead], Type[CVInsertIntoDB]]
) -> Union[CVFullRead, CVShortRead, CVInsertIntoDB]:
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


def b64_to_local_csv(title: str, b64_str: bytes) -> None:
    image_64_decode = base64.b64decode(b64_str)
    # create a writable image and write the decoding result
    image_result = open(title, 'wb')
    image_result.write(image_64_decode)


def clear_csv() -> None:
    """Deletes all local .csv"""
    removing_files = glob('./*.csv')
    for i in removing_files:
        os.remove(i)
    logging.info("ALL LOCAL .csv ARE CLEARED SUCCESSFULLY!")


def b64_to_file(b64_str: bytes, title: str = 'temp.csv') -> None:
    image_64_decode = base64.b64decode(b64_str)
    image_result = open(title, 'wb')
    image_result.write(image_64_decode)


def update_item_attrs(cv_id: str, model: CVUpdate):
    # Init expressions
    update_expression = "set"
    expression_attribute_values = {}
    attributes = model.dict()
    for key, value in attributes.items():
        if value:
            update_expression += f' {key} = :{key},'
            expression_attribute_values[f':{key}'] = value

    #   Cutting the last comma
    update_expression = update_expression[:-1]

    response = db_table.update_item(
        Key={'cv_id': cv_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return response
