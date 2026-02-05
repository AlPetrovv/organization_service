DC = docker compose
EXEC = docker exec -it

APP_CONTAINER_NAME = app
APP_SERVICE_NAME = organization-service

DB_CONTAINER_NAME = organization-service-db
DB_SERVICE_NAME = db



.PHONY: run
run: stop
	$(DC) up -d

.PHONY: stop
stop:
	$(DC) down

.PHONY: build
build:
	$(DC) build

.PHONY: shell
shell:
	$(EXEC) $(APP_CONTAINER_NAME) /bin/bash

.PHONY: db-run
db-run:
	$(DC) up $(DB_SERVICE_NAME) --build -d


.PHONY: db-stop
db-stop:
	$(DC) down $(DB_SERVICE_NAME)