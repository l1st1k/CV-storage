import logging
import uuid
from uuid import uuid4

from fastapi import HTTPException

__all__ = (
    'get_uuid',
    'check_for_404',
    'TableMixin',
)


#  Settings
logging.basicConfig(level=logging.DEBUG)


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())


def check_for_404(container, message: str = "Item can't be found!") -> None:
    """Checks container for 'empty' case"""
    if not len(container):
        raise HTTPException(
            status_code=404,
            detail=message
        )


class TableMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def get_session(cls):
        from main import get_ctx
        return get_ctx().get("sql_client").create_session()

    @classmethod
    def to_dict(cls, obj):
        return {k: (v if not isinstance(v, uuid.UUID) else str(v))
                for k, v in obj.__dict__.items()
                if not k.startswith('_')}
