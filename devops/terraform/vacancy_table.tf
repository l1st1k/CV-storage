resource "aws_dynamodb_table" "vacancy-dynamodb-table" {
  name           = "vacancy_table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "vacancy_id"

  attribute {
    name = "vacancy_id"
    type = "S"
  }

  tags = {
    Name        = "dynamodb-main-table"
    Environment = "production"
  }
}
