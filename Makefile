PROJECT-NAME = mindfulguard
VENV = $(PROJECT-NAME)-venv
INFO = $(PROJECT-NAME).egg-info
PIP-WIN = .\$(VENV)\Scripts\pip
PIP-LINUX = ./$(VENV)/bin/pip
VERSION = 3.10
PATH-TO-SOURCE = $(PROJECT-NAME)/

ACTIVATE-VENV-MSG = TO RUN, ENTER THE COMMAND
DEACTIVATE-VENV-MSG = TO DEACTIVATE, USE THE COMMAND "deactivate"

PORT = 8080
HOST = 0.0.0.0

PATH-TO-DB=db
PATH-TO-MIGRATIONS=$(PATH-TO-DB)/migrations

#docker
DOCKER_WORK_DIR = docker
DOCKER_COMPOSE_YML= $(DOCKER_WORK_DIR)/docker-compose.yml

ifeq ($(OS),Windows_NT)
    RM = rmdir /s /q
	SETUP-VENV = python -m venv $(VENV)
	RUN-VENV = $(ACTIVATE-VENV-MSG) .\$(VENV)\Scripts\activate
else
    RM = rm -rf
	SETUP-VENV = python$(VERSION) -m venv $(VENV)
	RUN-VENV = $(ACTIVATE-VENV-MSG) "source $(VENV)/bin/activate"

	MIGRATION-UP=bash ./$(PATH-TO-DB)/migration.sh $(PATH-TO-MIGRATIONS) up ${POSTGRES_USER} ${POSTGRES_PASSWORD} ${POSTGRES_HOST} ${POSTGRES_PORT} ${POSTGRES_DB}
	MIGRATION-DOWN=bash ./$(PATH-TO-DB)/migration.sh $(PATH-TO-MIGRATIONS) down ${POSTGRES_USER} ${POSTGRES_PASSWORD} ${POSTGRES_HOST} ${POSTGRES_PORT} ${POSTGRES_DB}
endif

setup:
	$(SETUP-VENV)
	@echo *****$(RUN-VENV)*****
	@echo *****make pip-i*****
	@echo *****docker-compose -f $(DOCKER_COMPOSE_YML) up -d*****
	@echo *****$(DEACTIVATE-VENV-MSG)*****

pip-i:
	pip install -e .

run:
	python $(PROJECT-NAME)/__main__.py --host $(HOST) --port $(PORT) ${MINDFULGUARD_ARGS}

test:
	pytest

migration-up:
	$(MIGRATION-UP)

migration-down:
	$(MIGRATION-DOWN)

clean:
	$(RM) $(INFO)
	$(RM) $(VENV)