import logging

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from core.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
from integrations.sql.sqlalchemy_base import Base

# Don't delete imports (required for table creation process)
from modules.cv.table import CvTable


logger = logging.getLogger(__name__)


class SQL_Client:
    _instance = None
    sql_url = ""

    @classmethod
    def get_url(cls):
        cls.sql_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB}"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SQL_Client, cls).__new__(cls)
            cls.get_url()
            cls._instance.engine = create_engine(
                cls.sql_url,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                # echo=True
            )

        return cls._instance

    def create_session(self) -> Session:
        session = sessionmaker(bind=self.engine)()

        return session


sql_client = None


def initialize(app: FastAPI):
    global sql_client
    logger.info("Initializing SQL connection...")
    sql_client = SQL_Client()
    Base.metadata.create_all(sql_client.engine)
    logger.info("SQL initialized!")