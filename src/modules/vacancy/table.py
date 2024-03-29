import uuid
from typing import Optional, Type

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.services_general import (NO_PERMISSION_EXCEPTION, TableMixin,
                                   check_for_404)
from integrations.sql.sqlalchemy_base import Base
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
        with cls.session_manager() as session:
            from modules.company.table import CompanyTable
            company: CompanyTable = CompanyTable.get_company_by_token_id(id_from_token)
            session.add(company)

            if item_specific:
                vacancy_ids = [vacancy.vacancy_id for vacancy in company.vacancies]
                if uuid.UUID(vacancy_id) not in vacancy_ids:
                    raise NO_PERMISSION_EXCEPTION

            return str(company.company_id)

    @classmethod
    def create(cls, model: VacancyInsertAndFullRead) -> Optional[str]:
        with cls.session_manager() as session:
            obj = cls.from_model(model)
            session.add(obj)

            return model.vacancy_id

    @classmethod
    def retrieve(cls, vacancy_id: str) -> VacancyInsertAndFullRead:
        with cls.session_manager() as session:
            row: Type[VacancyTable] = session.query(cls).filter_by(vacancy_id=uuid.UUID(vacancy_id)).first()
            check_for_404(row, "No vacancy with such ID")

            return VacancyInsertAndFullRead(**cls.to_dict(row))

    @classmethod
    def update(cls, attrs: dict) -> None:
        with cls.session_manager() as session:
            row: Type[VacancyTable] = session.query(cls).filter_by(
                vacancy_id=uuid.UUID(attrs.get("vacancy_id"))
            ).first()
            check_for_404(row, "No vacancy with such ID")
            attrs.pop("vacancy_id")
            for field, value in attrs.items():
                if value:
                    setattr(row, field, value)

    @classmethod
    def delete(cls, vacancy_id: str) -> None:
        with cls.session_manager() as session:
            row: Type[VacancyTable] = session.query(cls).filter_by(vacancy_id=uuid.UUID(vacancy_id)).first()
            check_for_404(row, "No vacancy with such ID")
            session.delete(row)
