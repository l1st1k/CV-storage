from fastapi import FastAPI, UploadFile, status
from fastapi.responses import JSONResponse

from models import CVUpdate, CVFullRead, CVInsertIntoDB, CVsRead
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


@app.post(
    "/cv",
    response_class=JSONResponse,
    description='Upload CV in .csv',
    tags=[
        "CV"
    ]
)
def _post_cv(file: UploadFile):
    return CVRepository.create(file=file)


@app.patch(
    "/cv/{cv_id}",
    response_model=CVFullRead,
    description="Updates CV by ID",
    tags=[
        "CV"
    ]
)
def _update_cv(cv_id: str, model: CVUpdate):
    return CVRepository.update(cv_id=cv_id, data=model)


# TODO get for .csv files