# CV-storage (Backend)
Project for storing and sharing IT cvs. <br /> 
Stack: Python, FastAPI, DynamoDB, Terraform, LocalStack, boto3.

### Commands to start the project:
`cd devops` - to enter devops directory<br />
`docker-compose up -d` - to start container with localstack<br /> 
`terraform apply -auto-approve` - to create DynamoDB table<br /> 
`cd ../src` - to enter main code directory<br />
`uvicorn main:app --reload` - to start FastAPI application

### [Swagger endpoint](http://127.0.0.1:8000/docs) 
