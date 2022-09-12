from models import CVUpdate

temp = CVUpdate(
    first_name='sashka'
)
ID = 'e097f005-144f-470a-ae81-5a70a5405b8b'
from database import db_table


def get_update_params(body):
    """Given a dictionary we generate an update expression and a dict of values
    to update a dynamodb table.

    Params:
        body (dict): Parameters to use for formatting.

    Returns:
        update expression, dict of values.
    """
    update_expression = ["set "]
    update_values = dict()

    for key, val in body.items():
        update_expression.append(f" {key} = :{key},")
        update_values[f":{key}"] = val

    return "".join(update_expression)[:-1], update_values


def update(body):
    a, v = get_update_params(body)
    print(a, v, sep='\n')
    response = db_table.update_item(
        Key={'cv_id': ID},
        UpdateExpression=a,
        ExpressionAttributeValues=dict(v)
    )
    return response


# Init update-expression
update_expression = "set"
expression_attribute_names = {}
expression_attribute_values = {}
attributes = temp.dict()

for key, value in attributes.items():
    if value:
        update_expression += f' {key} = :{key},'
        expression_attribute_values[f':{key}'] = value

#   Cutting the last comma
update_expression = update_expression[:-1]

print(update_expression, expression_attribute_values, sep='\n')

response = db_table.update_item(
                Key={'cv_id':  ID},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
)

print(response)
