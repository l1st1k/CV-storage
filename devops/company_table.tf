resource "aws_dynamodb_table" "company-dynamodb-table" {
  name           = "company_table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "company_id"

  attribute {
    name = "company_id"
    type = "S"
  }

  tags = {
    Name        = "dynamodb-main-table"
    Environment = "production"
  }
}
