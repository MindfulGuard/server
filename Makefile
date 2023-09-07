PROJECT-NAME = mypass
VENV = $(PROJECT-NAME)-venv
INFO = $(PROJECT-NAME).egg-info
PIP-WIN = .\$(VENV)\Scripts\pip
PIP-LINUX = ./$(VENV)/bin/pip
VERSION = 3.10
PATH-TO-SOURCE = $(PROJECT-NAME)/
REQUIREMENTS = requirements.txt

ACTIVATE-VENV-MSG = TO RUN, ENTER THE COMMAND
DEACTIVATE-VENV-MSG = TO DEACTIVATE, USE THE COMMAND "deactivate"

PORT = 8080
HOST = 0.0.0.0

#docker
CONTAINER_NAME = docker-db-1
DATABASE_USERS = mypass
DATABASE_NAME = mypass
PATH-TO-DUMP = docker/dumps/pgsql.sql

ifeq ($(OS),Windows_NT)
    RM = rmdir /s /q

	SETUP-VENV = py -$(VERSION) -m venv $(VENV)
	PIP-VENV = $(PIP-WIN) install -r $(REQUIREMENTS)
	RUN-VENV = $(ACTIVATE-VENV-MSG) .\$(VENV)\Scripts\activate

	UPDATE-LIST = $(PIP-WIN) freeze > $(REQUIREMENTS)
else
    RM = rm -rf

	SETUP-VENV = python$(VERSION) -m venv $(VENV)
	PIP-VENV  = $(PIP-LINUX) install -r $(REQUIREMENTS)
	RUN-VENV = $(ACTIVATE-VENV-MSG) "source $(VENV)/bin/activate"

	UPDATE-LIST = $(PIP-LINUX) freeze > $(REQUIREMENTS)
endif

setup:
	$(SETUP-VENV)
	@echo *****$(RUN-VENV)*****
	@echo *****make pip-i*****
	@echo *****docker-compose up -d*****
	@echo *****$(DEACTIVATE-VENV-MSG)*****

pip-i:
	pip install -e .

run:
	uvicorn $(PROJECT-NAME).__main__:app --host $(HOST) --port $(PORT)
test:
	pytest
docker-dump:
	docker exec -t $(CONTAINER_NAME) pg_dump -U $(DATABASE_USERS) $(DATABASE_NAME) > $(PATH-TO-DUMP)

clean:
	$(RM) $(INFO)
	$(RM) $(VENV)