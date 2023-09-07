VENV = mypass-venv
INFO = mypass.egg-info
PIP-WIN = .\$(VENV)\Scripts\pip
PIP-LINUX = ./$(VENV)/bin/pip
VERSION = 3.10
PATH-TO-SOURCE = mypass/
REQUIREMENTS = requirements.txt

ACTIVATE-VENV-MSG = TO RUN, ENTER THE COMMAND
DEACTIVATE-VENV-MSG = TO DEACTIVATE, USE THE COMMAND "deactivate"

PORT = 8080
HOST = 0.0.0.0

#docker
CONTAINER_NAME = docker-db-1
DATABASE_USERS = mypass
DATABASE_NAME = mypass

ifeq ($(OS),Windows_NT)
    RM = rmdir /s /q

	SETUP-VENV = py -$(VERSION) -m venv $(VENV)
	PIP-VENV = $(PIP-WIN) install -r $(REQUIREMENTS)
	RUN-VENV = $(ACTIVATE-VENV-MSG) .\mypass-venv\Scripts\activate

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
	@echo *****$(DEACTIVATE-VENV-MSG)*****

pip-i:
	pip install -e .

run:
	uvicorn mypass.__main__:app --host $(HOST) --port $(PORT)
test:
	pytest
docker-dump:
	docker exec -t $(CONTAINER_NAME) pg_dump -U $(DATABASE_USERS) $(DATABASE_NAME) > docker/dumps/pgsql.sql

clean:
	$(RM) $(INFO)
	$(RM) $(VENV)