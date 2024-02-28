from typing import Optional

from sqlalchemy import Column, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID

# from integrations.sql import sql_client
from integrations.sql.sqlalchemy_base import Base
from modules.cv.models import CVsFullRead


global sql_client


class CvTable(Base):
    __tablename__ = "cv"

    cv_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), nullable=False)
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

    @classmethod
    def get_request(cls, url: str):
        """Retrieves request data by URL"""
        session = sql_client.create_session()
        session.close()
    #
    #     try:
    #         sql_expression = text(
    #             f"SELECT * FROM {cls.__tablename__} WHERE :url REGEXP {cls.__tablename__}.url_regex LIMIT 1"
    #         )
    #         request = session.execute(sql_expression, {"url": url}).fetchone()
    #         return RequestData.from_row(request) if request else None
    #     except:
    #         session.rollback()
    #         raise
    #     finally:
    #         session.close()
