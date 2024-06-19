PROJECT-NAME = mindfulguard
VENV = $(PROJECT-NAME)-venv
INFO = $(PROJECT-NAME).egg-info
PIP-WIN = .\$(VENV)\Scripts\pip
PIP-LINUX = ./$(VENV)/bin/pip
VERSION = 3.10
PATH-TO-SOURCE = $(PROJECT-NAME)/
ACTIVATE-VENV-MSG = TO RUN VENV, ENTER THE COMMAND

PORT = 8080
HOST = 0.0.0.0

PATH-TO-DB=db
PATH-TO-MIGRATIONS=$(PATH-TO-DB)/migrations

ifeq ($(OS),Windows_NT)
    RM = rmdir /s /q
	SETUP-VENV = python -m venv $(VENV)
	PIP-VENV = $(PIP-WIN)
	RUN-VENV = $(ACTIVATE-VENV-MSG) .\$(VENV)\Scripts\activate
else
    RM = rm -rf
	SETUP-VENV = python$(VERSION) -m venv $(VENV)
	PIP-VENV = $(PIP-LINUX)
	RUN-VENV = $(ACTIVATE-VENV-MSG) "source $(VENV)/bin/activate"

	MIGRATION-UP=bash ./$(PATH-TO-DB)/migration.sh $(PATH-TO-MIGRATIONS) up ${POSTGRES_USER} ${POSTGRES_PASSWORD} ${POSTGRES_HOST} ${POSTGRES_PORT} ${POSTGRES_DB}
	MIGRATION-DOWN=bash ./$(PATH-TO-DB)/migration.sh $(PATH-TO-MIGRATIONS) down ${POSTGRES_USER} ${POSTGRES_PASSWORD} ${POSTGRES_HOST} ${POSTGRES_PORT} ${POSTGRES_DB}
endif

bootstrap:
	pip install -e .

bootstrap-venv:
	$(SETUP-VENV)
	$(PIP-VENV) install -e .
	@echo *****$(RUN-VENV)*****

run:
	python $(PROJECT-NAME)/__main__.py --host $(HOST) --port $(PORT) ${MINDFULGUARD_ARGS}

test:
	python -m pytest

migration-up:
	$(MIGRATION-UP)

migration-down:
	$(MIGRATION-DOWN)

PROTO-GEN-OUT-PATH = $(PATH-TO-SOURCE)grpc/gen
PROTO-FILES-DIR-DYNAMIC-CONFIGURATIONS = services/configuration/grpc/dynamic_configurations

.PHONY: gen-proto
gen-proto:
	python -m grpc_tools.protoc -I $(PROTO-FILES-DIR-DYNAMIC-CONFIGURATIONS) --python_out=$(PROTO-GEN-OUT-PATH) --pyi_out=$(PROTO-GEN-OUT-PATH) --grpc_python_out=$(PROTO-GEN-OUT-PATH) $(PROTO-FILES-DIR-DYNAMIC-CONFIGURATIONS)/*.proto

clean:
	$(RM) $(INFO)
	$(RM) $(VENV)