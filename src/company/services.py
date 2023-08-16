import logging

from database import company_table

from company.models import CompanyUpdate, CompanyInsertAndFullRead

__all__ = (

)


#  Settings
logging.basicConfig(level=logging.INFO)
