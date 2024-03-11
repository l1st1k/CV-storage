import uuid
from typing import Optional, Type

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.services_general import check_for_404, TableMixin, NO_PERMISSION_EXCEPTION
from integrations.sql.sqlalchemy_base import Base
from modules.company.table import CompanyTable
from modules.vacancy.models import VacancyInsertAndFullRead


class VacancyTable(Base, TableMixin):
    __tablename__ = "vacancy"

    vacancy_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.company_id'), nullable=False)
    major = Column(String(length=63), nullable=False)
    years_of_exp = Column(Integer, nullable=False)
    skills = Column(String(length=255), nullable=True)

    # Relationship
    company = relationship("CompanyTable", back_populates="vacancies")

    @classmethod
    def from_model(cls, model: VacancyInsertAndFullRead):
        return cls(
            vacancy_id=uuid.UUID(model.vacancy_id),
            company_id=uuid.UUID(model.company_id),
            major=model.major,
            years_of_exp=model.years_of_exp,
            skills=model.skills if model.skills else None
        )

    @classmethod
    def check_token_permission(
            cls,
            id_from_token: str,
            vacancy_id: str = None,
            item_specific: bool = True
    ) -> str:
        company: CompanyTable = CompanyTable.get_company_by_token_id(id_from_token)

        if item_specific:
            vacancy_ids = [vacancy.vacancy_id for vacancy in company.vacancies]
            if vacancy_id not in vacancy_ids:
                raise NO_PERMISSION_EXCEPTION

        return company.company_id
    #
    # @classmethod
    # def create(cls, model: CVInsertIntoDB) -> Optional[str]:
    #     with cls.session_manager() as session:
    #         obj = cls.from_model(model)
    #         session.add(obj)
    #
    #         return model.cv_id
    #
    # @classmethod
    # def retrieve(cls, cv_id: str) -> CVFullRead:
    #     with cls.session_manager() as session:
    #         row: Type[CvTable] = session.query(cls).filter_by(cv_id=uuid.UUID(cv_id)).first()
    #         check_for_404(row, "No CV with such ID")
    #
    #         return CVFullRead(**cls.to_dict(row))
    #
    # @classmethod
    # def get_updated_model(cls, cv_id: str, data: CVUpdate) -> CVFullRead:
    #     model: CVFullRead = cls.retrieve(cv_id)
    #     updated_fields = data.dict(exclude_none=True)
    #     updated_model = model.copy(update=updated_fields)
    #
    #     return updated_model
    #
    # @classmethod
    # def update(cls, model: CVInsertIntoDB) -> CVFullRead:
    #     with cls.session_manager() as session:
    #         row: Type[CvTable] = session.query(cls).filter_by(cv_id=uuid.UUID(model.cv_id)).first()
    #         check_for_404(row, "No CV with such ID")
    #         for field, value in model.dict(exclude={'cv_id'}).items():
    #             setattr(row, field, value)
    #
    #         return CVFullRead(**cls.to_dict(row))
    #
    # @classmethod
    # def delete(cls, cv_id: str) -> None:
    #     with cls.session_manager() as session:
    #         cv_row: Type[CvTable] = session.query(cls).filter_by(cv_id=uuid.UUID(cv_id)).first()
    #         check_for_404(cv_row, "No CV with such ID")
    #         session.delete(cv_row)
