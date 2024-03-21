import logging
import uuid
from typing import Optional, Type

from sqlalchemy import Column, String, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.services_general import check_for_404, TableMixin, NO_PERMISSION_EXCEPTION
from integrations.sql.sqlalchemy_base import Base
from modules.manager.models import ManagerInsertAndFullRead, ManagerShortRead


class ManagerTable(Base, TableMixin):
    __tablename__ = "manager"

    manager_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.company_id'), nullable=False)
    email = Column(String(length=31), nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)

    # Relationship
    company = relationship("CompanyTable", back_populates="managers")

    @classmethod
    def from_model(cls, model: ManagerInsertAndFullRead):
        return cls(
            manager_id=uuid.UUID(model.manager_id),
            company_id=uuid.UUID(model.company_id),
            email=model.email,
            hashed_password=model.hashed_password,
            salt=model.salt
        )

    @classmethod
    def check_token_permission(
            cls,
            id_from_token: str,
            manager_id: str = None,
            item_specific: bool = True
    ) -> str:
        with cls.session_manager() as session:
            from modules.company.table import CompanyTable
            company: CompanyTable = CompanyTable.get_company_by_token_id(id_from_token)
            session.add(company)

            if item_specific:
                manager_ids = [manager.manager_id for manager in company.managers]
                if uuid.UUID(manager_id) not in manager_ids:
                    raise NO_PERMISSION_EXCEPTION

            return str(company.company_id)

    @classmethod
    def get_manager_by_email(cls, email: str) -> ManagerInsertAndFullRead:
        with cls.session_manager() as session:
            manager_row: Type[ManagerTable] = session.query(cls).filter_by(email=email).first()
            check_for_404(manager_row, "No Manager with such email")
            return ManagerInsertAndFullRead(**cls.to_dict(manager_row))

    @classmethod
    def create(cls, model: ManagerInsertAndFullRead) -> Optional[str]:
        with cls.session_manager() as session:
            obj = cls.from_model(model)
            session.add(obj)
            logging.info(f"Registered new manager: '{model.email}'!")
            return model.manager_id

    @classmethod
    def retrieve(cls, manager_id: str) -> ManagerShortRead:
        with cls.session_manager() as session:
            row: Type[ManagerTable] = session.query(cls).filter_by(manager_id=uuid.UUID(manager_id)).first()
            check_for_404(row, "No manager with such ID")

            return ManagerShortRead(**cls.to_dict(row))
    #
    # @classmethod
    # def update(cls, model: CVInsertIntoDB) -> CVFullRead:
    #     with cls.session_manager() as session:
    #         row: Type[CvTable] = session.query(cls).filter_by(cv_id=uuid.UUID(model.cv_id)).first()
    #         check_for_404(row, "No CV with such ID")
    #         for field, value in model.dict(exclude={'cv_id'}).items():
    #             setattr(row, field, value)
    #
    #         return CVFullRead(**cls.to_dict(row))
    #
    # @classmethod
    # def delete(cls, cv_id: str) -> None:
    #     with cls.session_manager() as session:
    #         cv_row: Type[CvTable] = session.query(cls).filter_by(cv_id=uuid.UUID(cv_id)).first()
    #         check_for_404(cv_row, "No CV with such ID")
    #         session.delete(cv_row)
