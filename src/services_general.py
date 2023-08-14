import logging
from uuid import uuid4

from fastapi import HTTPException

__all__ = (
    'get_uuid',
    'check_for_404',
    'check_for_404_with_item',
)


#  Settings
logging.basicConfig(level=logging.INFO)


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())


def check_for_404(container, message: str = "Item can't be found!"):
    """Checks container for 'empty' case"""
    if len(container) == 0:
        raise HTTPException(
            status_code=404,
            detail=message
        )


def check_for_404_with_item(container, item, message: str = "Item can't be found!"):
    """
    Checks response for 'empty' case
    Used only for checking responses of .get_item() function
    """
    if item not in container:
        raise HTTPException(
            status_code=404,
            detail=message
        )
