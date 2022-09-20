provider "aws" {

  access_key                  = "foo"
  secret_key                  = "foo"
  region                      = "eu-central-1"

  s3_use_path_style         = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    dynamodb             = "http://localhost:4566"
  }
}
