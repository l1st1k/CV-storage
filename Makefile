.PHONY: setup start-localstack create-dynamodb start-fastapi start

# Target to set up the entire project
setup:
	$(MAKE) start-localstack
	$(MAKE) create-dynamodb
	$(MAKE) start-fastapi

# Target to start only localstack and FastAPI
start:
	$(MAKE) start-localstack
	$(MAKE) start-fastapi

start-localstack:
	cd devops && docker compose up -d

create-dynamodb:
	cd devops && terraform apply -auto-approve

start-fastapi:
	sudo lsof -t -i tcp:8000 | xargs kill -9
	cd src && uvicorn main:app --reload
