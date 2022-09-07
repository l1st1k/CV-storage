from fastapi import FastAPI

from database import db_table
from models import CVCreate, CVInsertIntoDB, CVsRead, CVFullRead
from repository import CVRepository

app = FastAPI()


@app.get(
    "/cvs",
    response_model=CVsRead,
    description="List all the CVs",
    tags=[
        "CVs"
    ]
)
def _list_cvs():
    return CVRepository.list()


@app.get(
    "/cv/{cv_id}",
    response_model=CVFullRead,
    description="Retrieve CV by ID",
    tags=[
        "CV"
    ]
)
def _get_cv(cv_id: str):
    return CVRepository.get(cv_id=cv_id)


# db_table.put_item(Item=dict(TEMP_INTO_DB_MODEL))
# response = db_table.scan()
