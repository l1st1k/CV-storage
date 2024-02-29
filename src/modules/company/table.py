from typing import Optional

from sqlalchemy import Column, Integer, String, text, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from integrations.sql.sqlalchemy_base import Base
from modules.company.models import CompanyInsertAndFullRead

global sql_client


class CompanyTable(Base):
    __tablename__ = "company"

    company_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_name = Column(String(length=20), nullable=False)
    email = Column(String(length=255), nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)
    logo_in_bytes = Column(String, nullable=True)  # Assuming base64 encoded string

    # Relationships
    cvs = relationship("CvTable", back_populates="company")
    # managers = relationship("ManagerTable", back_populates="company")
    # vacancies = relationship("VacancyTable", back_populates="company")
