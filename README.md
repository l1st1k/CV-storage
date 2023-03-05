# CV-storage (Backend)
Project for storing and sharing IT cvs. <br /> 
Stack: Python, FastAPI, DynamoDB, Terraform, LocalStack, boto3.

### Commands to start the project:

`docker-compose up -d` - to start container with localstack<br /> 
`terraform apply -auto-approve` - to create DynamoDB table<br /> 
`uvicorn main:app --reload` - to start FastAPI application

### [Swagger](127.0.0.1:8000/docs) endpoint

### .env-file: 
DYNAMODB_ENDPOINT=http://localhost:4566/ <br /> 
AWS_ACCESS_KEY=foo<br /> 
AWS_SECRET_ACCESS_KEY=foo<br /> 
AWS_REGION=eu-central-1<br /> 

