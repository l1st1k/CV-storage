from fastapi import FastAPI, Query, UploadFile
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import CVFullRead, CVsFullRead, CVsRead, CVUpdate
from repository import CVRepository

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get(
    "/cvs",
    response_model=CVsRead,
    description="List all the CVs",
    tags=[
        "CV"
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


@app.get(
    "/cv/{cv_id}/csv",
    response_class=FileResponse,
    description='Returns CV in .csv file',
    tags=[
        "CV"
    ]
)
def _get_csv(cv_id: str):
    return CVRepository.get_csv(cv_id=cv_id)


@app.delete(
    "/cv/{cv_id}",
    response_class=JSONResponse,
    description='Deletes CV from database',
    tags=[
        "CV"
    ]
)
def _delete_csv(cv_id: str):
    return CVRepository.delete(cv_id=cv_id)


@app.get(
    "/cvs/search",
    response_model=CVsFullRead,
    description='Searches for CV with necessary skills',
    tags=[
        "CV"
    ]
)
def _search_cvs(
        skill: str = Query(default=''),
        last_name: str = Query(default='', max_length=25),
        major: str = Query(default='', max_length=25)
):
    skill = skill.lower()
    last_name = last_name.lower()
    major = major.lower()
    return CVRepository.search(skill=skill, last_name=last_name, major=major)
