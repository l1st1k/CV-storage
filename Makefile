.PHONY:  start db web stop stop-db stop-web

start:
	$(MAKE) db
	$(MAKE) start-fastapi

db:
	cd devops && docker-compose up -d

web:
	cd src && uvicorn main:app --reload

stop-web:
	sudo lsof -t -i tcp:8000 | xargs kill -9

stop-db:
	cd devops && docker-compose stop

stop:
	$(MAKE) stop-web
	$(MAKE) stop-db
