.PHONY:  upd up stop

upd:
	cd devops && docker-compose up

up:
	cd devops && docker-compose up -d

stop:
	cd devops && docker-compose stop
