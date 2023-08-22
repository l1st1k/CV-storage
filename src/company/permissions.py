from database import company_table


__all__ = (
    'is_company_owner',
)


def is_company_owner(email: str, company_id: str) -> bool:
    response = company_table.get_item(
        Key={
            'company_id': company_id
        }
    )
    user_dict = response['Item']
    return email == user_dict['email']
