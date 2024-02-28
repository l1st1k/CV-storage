from fastapi import Query, UploadFile, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi_jwt_auth import AuthJWT

from modules.cv.models import CVsRead, CVFullRead, CVsFullRead, CVUpdate
from modules.cv.repository import CVRepository


class CVRouter:
    tags = ("CV",)
    
    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        self.app.get("/cvs", response_model=CVsRead, tags=self.tags)(self.list_cvs)
        self.app.get("/cv/{cv_id}", response_model=CVFullRead, tags=self.tags)(self.get_cv)
        self.app.post("/cv", response_class=JSONResponse, tags=self.tags)(self.post_cv)
        self.app.patch("/cv/{cv_id}", response_model=CVFullRead, tags=self.tags)(self.update_cv)
        self.app.get("/cv/{cv_id}/csv", response_class=FileResponse, tags=self.tags)(self.get_csv)
        self.app.delete("/cv/{cv_id}", response_class=JSONResponse, tags=self.tags)(self.delete_cv)
        self.app.get("/cvs/search", response_model=CVsFullRead, tags=self.tags)(self.search_cvs)

    @staticmethod
    async def list_cvs(Authorize: AuthJWT = Depends()) -> CVsFullRead:
        return CVRepository.list(Authorize=Authorize)

    @staticmethod
    async def get_cv(cv_id: str) -> CVFullRead:
        return CVRepository.get(cv_id=cv_id)

    @staticmethod
    async def post_cv(file: UploadFile, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return CVRepository.create(file=file, Authorize=Authorize)

    @staticmethod
    async def update_cv(cv_id: str, model: CVUpdate) -> CVFullRead:
        return CVRepository.update(cv_id=cv_id, data=model)

    @staticmethod
    async def get_csv(cv_id: str) -> FileResponse:
        return CVRepository.get_csv(cv_id=cv_id)

    @staticmethod
    async def delete_cv(cv_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        return CVRepository.delete(cv_id=cv_id, Authorize=Authorize)

    @staticmethod
    async def search_cvs(skill: str = Query(default=''), last_name: str = Query(default='', max_length=25),
                         major: str = Query(default='', max_length=25)) -> CVsFullRead:
        skill = skill.lower()
        last_name = last_name.lower()
        major = major.lower()
        return CVRepository.search(skill=skill, last_name=last_name, major=major)