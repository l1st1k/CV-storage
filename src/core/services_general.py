import logging
import uuid
from contextlib import contextmanager
from uuid import uuid4

import psycopg2
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

__all__ = (
    'NO_PERMISSION_EXCEPTION',
    'get_uuid',
    'check_for_404',
    'TableMixin',
)


#  Settings
logging.basicConfig(level=logging.INFO)

NO_PERMISSION_EXCEPTION = HTTPException(status_code=403, detail='No permissions')


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())


def check_for_404(item, message: str = "Item can't be found!") -> None:
    """Checks object/container for 'empty' case"""
    exc = HTTPException(status_code=404, detail=message)
    if hasattr(item, "len"):
        # Container case
        if not len(item):
            raise exc
    elif not item:
        # Object case
        raise exc


class TableMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def get_session(cls) -> Session:
        from main import get_ctx
        return get_ctx().get("sql_client").create_session()

    @classmethod
    @contextmanager
    def session_manager(cls):
        session: Session = cls.get_session()
        try:
            yield session
            session.commit()
        except IntegrityError as e:
            if 'violates unique constraint' in str(e.orig):
                raise HTTPException(status_code=400, detail=f"Account with such email already exists!")
            else:
                logging.error(e)
                raise HTTPException(status_code=500, detail="An unexpected error occurred.")
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def to_dict(cls, obj):
        return {k: (v if not isinstance(v, uuid.UUID) else str(v))
                for k, v in obj.__dict__.items()
                if not k.startswith('_')}
