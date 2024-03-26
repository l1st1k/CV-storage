import uuid
from typing import Optional, Type

from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.services_general import (NO_PERMISSION_EXCEPTION, TableMixin,
                                   check_for_404)
from integrations.sql.sqlalchemy_base import Base
from modules.cv.models import CVFullRead, CVInsertIntoDB, CVUpdate
from modules.cv.services import b64_to_file


class CvTable(Base, TableMixin):
    __tablename__ = "cv"

    cv_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.company_id'), nullable=False)
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255), nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String(length=15), nullable=False)
    major = Column(String(length=255), nullable=False)
    years_of_exp = Column(Integer, nullable=False)
    skills = Column(String(length=500), nullable=False)
    projects = Column(String(length=500), nullable=True)
    project_amount = Column(Integer, nullable=False)
    cv_in_bytes = Column(LargeBinary, nullable=True)

    # Relationship
    company = relationship("CompanyTable", back_populates="cvs")

    @classmethod
    def from_model(cls, model: CVInsertIntoDB):
        return cls(
            cv_id=uuid.UUID(model.cv_id),
            company_id=uuid.UUID(model.company_id),
            first_name=model.first_name,
            last_name=model.last_name,
            age=model.age,
            phone_number=model.phone_number,
            major=model.major,
            years_of_exp=model.years_of_exp,
            skills=model.skills,
            projects=model.projects,
            project_amount=model.project_amount,
            cv_in_bytes=model.cv_in_bytes if model.cv_in_bytes else None
        )

    @classmethod
    def check_token_permission(
            cls,
            id_from_token: str,
            cv_id: str = None,
            item_specific: bool = True
    ) -> str:
        with cls.session_manager() as session:
            from modules.company.table import CompanyTable
            company: CompanyTable = CompanyTable.get_company_by_token_id(id_from_token)
            session.add(company)

            if item_specific:
                cv_ids = [cv.cv_id for cv in company.cvs]
                if uuid.UUID(cv_id) not in cv_ids:
                    raise NO_PERMISSION_EXCEPTION

            return str(company.company_id)

    @classmethod
    def create(cls, model: CVInsertIntoDB) -> Optional[str]:
        with cls.session_manager() as session:
            obj = cls.from_model(model)
            session.add(obj)

            return model.cv_id

    @classmethod
    def retrieve(cls, cv_id: str) -> CVFullRead:
        with cls.session_manager() as session:
            row: Type[CvTable] = session.query(cls).filter_by(cv_id=uuid.UUID(cv_id)).first()
            check_for_404(row, "No CV with such ID")

            return CVFullRead(**cls.to_dict(row))

    @classmethod
    def get_updated_model(cls, cv_id: str, data: CVUpdate) -> CVFullRead:
        model: CVFullRead = cls.retrieve(cv_id)
        updated_fields = data.dict(exclude_none=True)
        updated_model = model.copy(update=updated_fields)

        return updated_model

    @classmethod
    def update(cls, model: CVInsertIntoDB) -> CVFullRead:
        with cls.session_manager() as session:
            row: Type[CvTable] = session.query(cls).filter_by(cv_id=uuid.UUID(model.cv_id)).first()
            check_for_404(row, "No CV with such ID")
            for field, value in model.dict(exclude={'cv_id'}).items():
                setattr(row, field, value)

            return CVFullRead(**cls.to_dict(row))

    @classmethod
    def delete(cls, cv_id: str) -> None:
        with cls.session_manager() as session:
            cv_row: Type[CvTable] = session.query(cls).filter_by(cv_id=uuid.UUID(cv_id)).first()
            check_for_404(cv_row, "No CV with such ID")
            session.delete(cv_row)

    @classmethod
    def get_csv(cls, cv_id: str) -> str:
        with cls.session_manager() as session:
            cv_row: Type[CvTable] = session.query(cls).filter_by(cv_id=uuid.UUID(cv_id)).first()
            check_for_404(cv_row, "No CV with such ID")

            title = b64_to_file(cv_row.cv_in_bytes, title=cv_row.last_name + ".csv")

            return title
