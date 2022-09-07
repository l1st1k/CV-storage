from fastapi import FastAPI
from database import db_table
from models import (CVCreate,
                    CVInsertIntoDB,
                    CVsRead)
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










# db_table.put_item(Item=dict(TEMP_INTO_DB_MODEL))
# response = db_table.scan()
