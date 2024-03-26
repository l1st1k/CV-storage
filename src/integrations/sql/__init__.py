import logging

import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from core.config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER
from integrations.sql.sqlalchemy_base import Base
# Don't delete imports (required for table creation process)
# from modules.company.table import CompanyTable
from modules.cv.table import CvTable
from modules.manager.table import ManagerTable
from modules.vacancy.table import VacancyTable

logger = logging.getLogger(__name__)


class SQL_Client:
    _instance = None
    sql_url = ""

    @classmethod
    def get_url(cls):
        cls.sql_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SQL_Client, cls).__new__(cls)
            cls.get_url()
            cls._instance.engine = create_engine(
                cls.sql_url,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                # echo=True # Used for SQL query logging
            )

        return cls._instance

    def create_session(self) -> Session:
        session = sessionmaker(bind=self.engine)()

        return session


def initialize(app: FastAPI, ctx: dict):
    logger.info("Initializing SQL connection...")
    sql_client = SQL_Client()
    try:
        Base.metadata.create_all(sql_client.engine)
    except sqlalchemy.exc.OperationalError:
        logger.error("NO CONNECTION TO SQL DATABASE... Please, check, if its up!")
    else:
        ctx["sql_client"] = sql_client
        logger.info("SQL initialized!")
