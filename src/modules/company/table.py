import uuid
from typing import Optional, Type, List

from sqlalchemy import Column, Integer, String, text, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.services_general import TableMixin, check_for_404
from integrations.sql.sqlalchemy_base import Base
from modules.company.models import CompanyInsertAndFullRead
from modules.cv.models import CVsFullRead, CVFullRead

global sql_client


class CompanyTable(Base, TableMixin):
    __tablename__ = "company"

    company_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_name = Column(String(length=20), nullable=False)
    email = Column(String(length=255), nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)
    logo_in_bytes = Column(String, nullable=True)

    # Relationships
    cvs = relationship("CvTable", back_populates="company")
    # managers = relationship("ManagerTable", back_populates="company")
    # vacancies = relationship("VacancyTable", back_populates="company")

    @classmethod
    def get_cvs(cls, company_id: str) -> CVsFullRead:
        with cls.session_manager() as session:
            row: Type[CompanyTable] = session.query(cls).filter_by(company_id=uuid.UUID(company_id)).first()
            check_for_404(row, "No company with such ID")
            check_for_404(row.cvs, "No CVs in a company")
            return [CVFullRead(**cls.to_dict(document)) for document in row.cvs]
