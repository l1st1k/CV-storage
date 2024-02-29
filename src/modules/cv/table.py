import uuid
from typing import Optional

from sqlalchemy import Column, Integer, String, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Session


from integrations.sql.sqlalchemy_base import Base
from modules.cv.models import CVsFullRead, CVInsertIntoDB


class CvTable(Base):
    __tablename__ = "cv"

    @classmethod
    def get_session(cls):
        from main import get_ctx
        return get_ctx().get("sql_client").create_session()

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
    def add(cls, model: CVInsertIntoDB) -> Optional[str]:
        """Inserting CV model to DB"""
        session = cls.get_session()

        try:
            obj = cls.from_model(model)
            session.add(obj)
            session.commit()

            return model.cv_id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
