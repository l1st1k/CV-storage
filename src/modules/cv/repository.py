import logging
from base64 import b64encode

from fastapi_jwt_auth import AuthJWT

from modules.company.models import *
from modules.company.services import get_company_by_id
from fastapi import HTTPException, UploadFile, status, Depends
from fastapi.responses import FileResponse, JSONResponse
from core.services_general import check_for_404, get_uuid
from modules.company.table import CompanyTable
from modules.cv.models import CVsFullRead, CVFullRead, CVInsertIntoDB, CVUpdate
from modules.cv.services import b64_to_file, select_companys_cvs, csv_to_model, clear_csv, add_cv_to_company_model, \
    update_item_attrs, model_to_csv, update_encoded_string, delete_cv_from_db, delete_cv_from_company_model
from modules.cv.table import CvTable

from modules.vacancy.services import get_company_id

__all__ = (
    'CVRepository',
)


class CVRepository:
    @staticmethod
    def list(Authorize: AuthJWT = Depends()) -> CVsFullRead:
        # Authorize.jwt_required()
        # id_from_token = Authorize.get_jwt_subject()
        # company_id: str = get_company_id(id_from_token=id_from_token)
        company_id = "3422b448-2460-5fd2-9183-8999de6f8343"

        list_of_cvs: CVsFullRead = CompanyTable.get_cvs(company_id=company_id)

        return list_of_cvs

    @staticmethod
    def get(cv_id: str) -> CVFullRead:
        # Authorize.jwt_required()
        item = CvTable.retrieve(cv_id=cv_id)
        return item

    @staticmethod
    def create(file: UploadFile, Authorize: AuthJWT = Depends()) -> JSONResponse:
        """Uploads a CV and returns its id"""
        # Authorize.jwt_required()
        id_from_token = "3422b448-2460-5fd2-9183-8999de6f8343"

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
        model.company_id = id_from_token
        model.cv_in_bytes = encoded_string

        # Deleting local .csv
        clear_csv()

        # Database logic
        CvTable.create(model)

        # Logging
        logging.info(f"New CV received: {file.filename} for company(id = {id_from_token})")

        # Response
        response = JSONResponse(
            content={
                "message": f"New CV uploaded successfully!",
                "cv_id": model.cv_id,
                "company_id": model.company_id
            },
            status_code=status.HTTP_201_CREATED)

        return response

    @classmethod
    def update(cls, cv_id: str, data: CVUpdate) -> CVFullRead:
        pass
        # # Updating model's fields
        # update_item_attrs(cv_id, data)
        #
        # # Taking updated attrs in model
        # model: CVFullRead = cls.get(cv_id)
        #
        # # Writing local .csv with updated attrs
        # model_to_csv(model)
        #
        # # Reading .csv into base64
        # filename = model.last_name + '.csv'
        # with open(filename, "rb") as file:
        #     encoded_string = b64encode(file.read())
        # update_encoded_string(cv_id=cv_id, encoded_string=encoded_string)
        #
        # # Deleting local .csv
        # clear_csv()
        #
        # # Responding with the full model of updated items
        # return model

    @staticmethod
    def get_csv(cv_id: str) -> FileResponse:
        pass
        # # Querying from DB
        # document = cv_table.get_item(
        #     Key={
        #         'cv_id': cv_id
        #     },
        #     AttributesToGet=[
        #         'last_name', 'cv_in_bytes'
        #     ]
        # )
        #
        # # 404 validation
        # check_for_404_with_item(
        #     container=document,
        #     item='Item',
        #     message='CV not found.'
        # )
        #
        # # Taking data from response
        # title: str = document['Item']['last_name'] + '.csv'
        # cv_in_bytes: bytes = document['Item']['cv_in_bytes']
        #
        # # Writing local .csv
        # b64_to_file(bytes(cv_in_bytes), title=title)
        #
        # # Response (as a '.csv' file)
        # return FileResponse(title)

    @staticmethod
    def delete(cv_id: str, Authorize: AuthJWT = Depends()) -> JSONResponse:
        # Authorize.jwt_required()
        # id_from_token = Authorize.get_jwt_subject()
        # company_id: str = get_company_id(id_from_token=id_from_token)
        company_id: str = "3422b448-2460-5fd2-9183-8999de6f8343"

        CvTable.delete(cv_id=cv_id, company_id=company_id)

        # Response
        response = JSONResponse(
            content="CV successfully deleted!",
            status_code=status.HTTP_200_OK
        )
        return response

    @staticmethod
    def search(skill: str, last_name: str, major: str) -> CVsFullRead:
        pass
        # response_from_db = cv_table.scan()
        #
        # # Empty DB validation
        # check_for_404(response_from_db['Items'], message="There is no any CV's in database!")
        #
        # # Taking list of items from db_response
        # scan_result = [CVFullRead(**document) for document in response_from_db['Items']]
        #
        # # Filtering
        # result = [
        #     item for item in scan_result
        #     if (skill in item.skills.lower())
        #        and (last_name in item.last_name.lower())
        #        and (major in item.major.lower())
        # ]
        #
        # # Empty result list validation
        # check_for_404(result, message="No matches found!")
        #
        # return result
