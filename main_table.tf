resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "main_table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "cv_id"

  attribute {
    name = "cv_id"
    type = "S"
  }

  tags = {
    Name        = "dynamodb-main-table"
    Environment = "production"
  }
}
