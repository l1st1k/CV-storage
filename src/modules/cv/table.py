import uuid
from typing import Optional, Type

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.services_general import check_for_404, TableMixin, NO_PERMISSION_EXCEPTION
from integrations.sql.sqlalchemy_base import Base
from modules.cv.models import CVInsertIntoDB, CVFullRead


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
    cv_in_bytes = Column(String, nullable=True)

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
    def delete(cls, cv_id: str, company_id) -> None:
        with cls.session_manager() as session:
            cv_row: Type[CvTable] = session.query(cls).filter_by(cv_id=uuid.UUID(cv_id)).first()
            check_for_404(cv_row, "No CV with such ID")
            if str(cv_row.company_id) == company_id:
                session.delete(cv_row)
            else:
                raise NO_PERMISSION_EXCEPTION
