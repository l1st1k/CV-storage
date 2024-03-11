import logging
import uuid
from typing import Type, List, Optional

from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.services_general import TableMixin, check_for_404
from integrations.sql.sqlalchemy_base import Base
from modules.company.models import CompanyInsertAndFullRead, CompaniesRead, CompanyShortRead
from modules.cv.models import CVsFullRead, CVFullRead


logger = logging.getLogger(__name__)


class CompanyTable(Base, TableMixin):
    __tablename__ = "company"

    company_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_name = Column(String(length=20), nullable=False)
    email = Column(String(length=255), nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)
    logo_in_bytes = Column(LargeBinary, nullable=True)

    # Relationships
    cvs = relationship("CvTable", back_populates="company")
    managers = relationship("ManagerTable", back_populates="company")
    vacancies = relationship("VacancyTable", back_populates="company")

    @classmethod
    def from_model(cls, model: CompanyInsertAndFullRead):
        return cls(
            company_id=uuid.UUID(model.company_id),
            company_name=model.company_name,
            email=model.email,
            hashed_password=model.hashed_password,
            salt=model.salt,
            logo_in_bytes=model.logo_in_bytes if model.logo_in_bytes else None
        )

    @classmethod
    def get_companies(cls) -> CompaniesRead:
        with cls.session_manager() as session:
            rows: List[Type[CompanyTable]] = session.query(cls)
            check_for_404(rows, "There are no any companies in database")
            return [CompanyShortRead(**cls.to_dict(document)) for document in rows]

    @classmethod
    def get_cvs(cls, company_id: str) -> CVsFullRead:
        with cls.session_manager() as session:
            row: Type[CompanyTable] = session.query(cls).filter_by(company_id=uuid.UUID(company_id)).first()
            check_for_404(row, "No company with such ID")
            check_for_404(row.cvs, "No CVs in a company")
            return [CVFullRead(**cls.to_dict(document)) for document in row.cvs]

    @classmethod
    def get_company_by_token_id(cls, id_from_token):
        # TODO (Manager model required)
        pass

    @classmethod
    def create(cls, model: CompanyInsertAndFullRead) -> Optional[str]:
        with cls.session_manager() as session:
            obj = cls.from_model(model)
            session.add(obj)
            logging.info(f"New Company registered: {model.company_name}")
            return model.company_id
