import base64
import csv
import logging
import os
from glob import glob
from typing import Type, Union

from modules.cv.models import CVFullRead, CVInsertIntoDB, CVShortRead

__all__ = (
    'model_to_csv',
    'csv_to_model',
    'clear_csv',
    'b64_to_file',
)


def model_to_csv(model: CVFullRead) -> str:
    """Writes local .csv file from model"""
    cv_dict = dict(model)
    title = 'tmp/' + model.last_name + '.csv'
    with open(title, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(cv_dict.items())

    return title


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

    # Ensure the directory exists
    directory = "tmp/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Creates a writable image and writes the decoded result
    title = directory + title
    image_result = open(title, 'wb')
    image_result.write(image_64_decode)

    return title
