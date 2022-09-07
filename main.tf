provider "aws" {

  access_key                  = "foo"
  secret_key                  = "foo"
  region                      = "eu-central-1"

  s3_force_path_style         = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    dynamodb             = "http://localhost:4566"
  }
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "main_table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "cv_id"
  range_key      = "last_name"

  attribute {
    name = "cv_id"
    type = "S"
  }

  attribute {
    name = "last_name"
    type = "S"
  }

  attribute {
    name = "first_name"
    type = "S"
  }

  attribute {
    name = "age"
    type = "N"
  }

attribute {
    name = "major"
    type = "S"
  }

  attribute {
    name = "skills"
    type = "SS"
  }

  attribute {
    name = "years_of_exp"
    type = "N"
  }

  attribute {
    name = "phone_number"
    type = "S"
  }

  attribute {
    name = "projects"
    type = "SS"
  }

  attribute {
    name = "project_amount"
    type = "N"
  }

  attribute {
    name = "cv_in_bytes"
    type = "B"
  }

  tags = {
    Name        = "dynamodb-main-table"
    Environment = "production"
  }
}