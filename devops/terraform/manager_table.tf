resource "aws_dynamodb_table" "manager-dynamodb-table" {
  name           = "manager_table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "manager_id"

  attribute {
    name = "manager_id"
    type = "S"
  }

  tags = {
    Name        = "dynamodb-main-table"
    Environment = "production"
  }
}
