import logging
from base64 import b64encode

from fastapi import HTTPException, UploadFile, status, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi_jwt_auth import AuthJWT

from core.services_general import get_uuid
from modules.company.table import CompanyTable
from modules.cv.models import CVsFullRead, CVFullRead, CVInsertIntoDB, CVUpdate
from modules.cv.services import b64_to_file, csv_to_model, clear_csv, model_to_csv
from modules.cv.table import CvTable


class CVRepository:
    @staticmethod
    def list(Authorize: AuthJWT = Depends()) -> CVsFullRead:
        # Authorize.jwt_required()
        # id_from_token = Authorize.get_jwt_subject()
        # company_id = CvTable.check_token_permission(
        #     id_from_token=id_from_token,
        #     item_specific=False
        # )
        company_id = "3422b448-2460-5fd2-9183-8999de6f8343"

        list_of_cvs: CVsFullRead = CompanyTable.get_cvs(company_id=company_id)
        # list_of_cvs: CVsFullRead = CompanyTable.get_cvs(company_id=company.company_id)

        return list_of_cvs

    @staticmethod
    def get(cv_id: str, Authorize: AuthJWT = Depends()) -> CVFullRead:
        Authorize.jwt_required()
        id_from_token = Authorize.get_jwt_subject()
        CvTable.check_token_permission(cv_id=cv_id, id_from_token=id_from_token, item_specific=True)

        item = CvTable.retrieve(cv_id=cv_id)
        return item

    @staticmethod
    def create(file: UploadFile, Authorize: AuthJWT = Depends()) -> JSONResponse:
        """Uploads a CV and returns its id"""
        # Authorize.jwt_required()
        # id_from_token = Authorize.get_jwt_subject()
        # company_id = CvTable.check_token_permission(
        #     id_from_token=id_from_token,
        #     item_specific=False
        # )

        company_id = "322d40b3-d7a6-4dca-b95e-a93030481f35"

        # Type check
        if file and (file.content_type != 'text/csv'):
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail="CV should be in .csv format!")

        # .csv into base 64
        encoded_string: bytes = b64encode(file.file.read())

        # Writing local .csv
        b64_to_file(encoded_string)

        # Reading .csv into model
        model = csv_to_model(response_class=CVInsertIntoDB)
        model.cv_id = get_uuid()
        model.company_id = company_id
        model.cv_in_bytes = encoded_string

        # Deleting local .csv
        clear_csv()

        # Database logic
        CvTable.create(model)

        # Logging
        logging.info(f"New CV received: {file.filename} for company(id={company_id})")

        # Response
        response = JSONResponse(
            content={
                "message": f"New CV uploaded successfully!",
                "cv_id": model.cv_id,
                "company_id": model.company_id
            },
            status_code=status.HTTP_201_CREATED)

        return response

    @staticmethod
    def update(
            cv_id: str,
            data: CVUpdate,
            Authorize: AuthJWT = Depends()
    ) -> CVFullRead:
        # Authorize.jwt_required()
        # id_from_token = Authorize.get_jwt_subject()
        # CvTable.check_token_permission(cv_id=cv_id, id_from_token=id_from_token)

        # Updating model's fields
        model = CvTable.get_updated_model(cv_id, data)

        # Writing local .csv with updated attrs
        filename = model_to_csv(model)

        # Reading .csv into base64
        with open(filename, "rb") as file:
            encoded_string = b64encode(file.read())
        db_model = CVInsertIntoDB(**model.dict())
        db_model.cv_in_bytes = encoded_string

        # DB Update
        CvTable.update(db_model)

        # Deleting local .csv
        clear_csv()

        # Responding with the full model of updated items
        return model

    @staticmethod
    def get_csv(cv_id: str, Authorize: AuthJWT = Depends()) -> FileResponse:
        # Authorize.jwt_required()
        # id_from_token = Authorize.get_jwt_subject()
        # CvTable.check_token_permission(cv_id=cv_id, id_from_token=id_from_token)

        title = CvTable.get_csv(cv_id=cv_id)
        return FileResponse(title)

    @staticmethod
    def delete(cv_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        # Authorize.jwt_required()
        # id_from_token = Authorize.get_jwt_subject()
        # CvTable.check_token_permission(cv_id=cv_id, id_from_token=id_from_token)

        CvTable.delete(cv_id=cv_id)

        # Response
        response = JSONResponse(
            content="CV successfully deleted!",
            status_code=status.HTTP_200_OK
        )
        return response

    @staticmethod
    def search(
            skill: str,
            last_name: str,
            major: str,
            Authorize: AuthJWT = Depends()
    ) -> CVsFullRead:
        # Authorize.jwt_required()
        # id_from_token = Authorize.get_jwt_subject()
        # company_id = CvTable.check_token_permission(
        #     id_from_token=id_from_token,
        #     item_specific=False
        # )
        company_id = "3422b448-2460-5fd2-9183-8999de6f8343"

        list_of_cvs: CVsFullRead = CompanyTable.get_cvs(company_id=company_id)

        # Filtering
        result = [
            item for item in list_of_cvs
            if all(
                (skill.lower() in item.skills.lower(),
                 last_name.lower() in item.last_name.lower(),
                 major.lower() in item.major.lower())
            )
        ]

        return result
