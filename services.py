import csv
from models import CVInsertIntoDB, CVShortRead, CVFullRead


def model_to_csv(model) -> None:
    cv_dict = dict(model)
    with open('temp.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(cv_dict.items())


def csv_to_model(full: bool) -> CVFullRead or CVShortRead:
    cv_dict = dict()
    with open('temp.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            cv_dict.update({row[0]: row[1]})

    # Model choice
    if full:
        model = CVFullRead(**cv_dict)
    else:
        model = CVShortRead(**cv_dict)
    return model
