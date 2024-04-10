PROJECT-NAME = mindfulguard
VENV = $(PROJECT-NAME)-build-venv
DOCKER_WORK_DIR = docker

WIN_PATH = .\$(VENV)\Scripts
LINUX_PATH = ./$(VENV)/bin

#docker
CONTAINER_NAME = docker-postgresql-1
DATABASE_USER = mindfulguard
DATABASE_NAME = mindfulguard_production
PATH-TO-DUMP = $(DOCKER_WORK_DIR)/dumps/pgsql.sql

admin_login =
admin_password =
database_host =
database_port =
database_user =
database_password =
minio_hostname =
minio_root_access_key =
minio_root_secret_key =
minio_user_access_key =
minio_user_secret_key =

ifeq ($(OS),Windows_NT)
    RM = rmdir /s /q

	PATH_TO_PIP = $(WIN_PATH)\pip3.exe
	PATH_TO_PYTHON_VENV = $(WIN_PATH)\python.exe

	SETUP-VENV = python -m venv $(VENV)
	RUN-VENV = $(ACTIVATE-VENV-MSG) .\$(VENV)\Scripts\activate

	MINIO_INIT_USER = PowerShell.exe -ExecutionPolicy Bypass -File .\build\scripts\minio_init_user.ps1 "$(minio_hostname)" "$(minio_root_access_key)" "$(minio_root_secret_key)" "$(minio_user_access_key)" "$(minio_user_secret_key)"
else
    RM = rm -rf

	PATH_TO_PIP = $(LINUX_PATH)/pip3
	PATH_TO_PYTHON_VENV = $(LINUX_PATH)/python3

	SETUP-VENV = python3 -m venv $(VENV)
	RUN-VENV = $(ACTIVATE-VENV-MSG) "source $(VENV)/bin/activate"

	MINIO_INIT_USER = chmod +x build/scripts/minio_init_user.sh && build/scripts/minio_init_user.sh "$(minio_hostname)" "$(minio_root_access_key)" "$(minio_root_secret_key)" "$(minio_user_access_key)" "$(minio_user_secret_key)"
endif

init:
	$(SETUP-VENV)
	$(PATH_TO_PIP) install -r build/requirements.txt
	$(PATH_TO_PYTHON_VENV) build/scripts/mindfulguard_init_admin.py $(admin_login) $(admin_password) $(database_host) $(database_port) $(database_user) $(database_password)
	$(MINIO_INIT_USER)

database-dump:
	docker exec -t $(CONTAINER_NAME) pg_dump -U $(DATABASE_USER) $(DATABASE_NAME) > $(PATH-TO-DUMP)