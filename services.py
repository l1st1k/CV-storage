import csv
from models import TEMP_INTO_DB_MODEL, CVInsertIntoDB


def temp_func():
    with open('example_csv/person1.csv', newline='') as csvfile:
        a = csv.reader(csvfile, delimiter=',', quotechar='|')
        print(type(a))
        for row in a:
            print(row)


def inp(obj):
    with open('names.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=list(CVInsertIntoDB.schema()["properties"].keys()))
        writer.writeheader()
        for k, v in obj:
            writer.writerow({k: v})


def out():
    fieldnames = list(CVInsertIntoDB.schema()["properties"].keys())
    with open('names.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        cv_dict = {}
        for row, field in zip(reader, fieldnames):
            cv_dict[field] = row[field]
        model = CVInsertIntoDB(**cv_dict)
        print(model)


# inp(TEMP_INTO_DB_MODEL)
out()
