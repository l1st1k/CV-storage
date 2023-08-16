import logging

from database import company_table

from company.models import CompanyInsertAndFullRead, CompanyUpdate

__all__ = (

)


#  Settings
logging.basicConfig(level=logging.INFO)
