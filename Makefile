VENV = mypass-venv
PIP-WIN = .\$(VENV)\Scripts\pip
PIP-LINUX = ./$(VENV)/bin/pip
VERSION = 3.10
PATH-TO-SOURCE = src/
REQUIREMENTS = requirements.txt

ACTIVATE-VENV-MSG = TO RUN, ENTER THE COMMAND
DEACTIVATE-VENV-MSG = TO DEACTIVATE, USE THE COMMAND "deactivate"


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
	$(PIP-VENV)
	@echo *****$(RUN-VENV)*****
	@echo *****$(DEACTIVATE-VENV-MSG)*****

update-list:
	$(UPDATE-LIST)

clean:
	$(RM) $(VENV)