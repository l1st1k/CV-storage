import base64
import csv
import logging
import os
from glob import glob
from typing import Type, Union
from uuid import uuid4

from models import CVFullRead, CVInsertIntoDB, CVShortRead

__all__ = (
    'model_to_csv',
    'csv_to_model',
    'get_uuid',
    'b64_to_local_csv',
    'clear_csv',
    'b64_to_file'
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


def b64_to_file(b64_str: bytes) -> None:
    image_64_decode = base64.b64decode(b64_str)
    # create a writable image and write the decoding result
    image_result = open('temp.csv', 'wb')
    image_result.write(image_64_decode)
