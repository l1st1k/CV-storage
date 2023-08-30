from core.database import manager_table
from core.services_general import check_for_404
from manager.models import *


class ManagerRepository:
    @staticmethod
    def list() -> ManagersRead:
        # Scanning DB
        response = manager_table.scan()

        # Empty DB validation
        check_for_404(response['Items'], message="There are no any manager in this company.")

        return [ManagerShortRead(**document) for document in response['Items']]
