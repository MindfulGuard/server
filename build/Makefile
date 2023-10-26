POSTGRES_PASSWORD = 12345678
POSTGRES_PASSWORD_USER = user1
POSTGRES_PASSWORD_PASSWORD = 123456

PROJECT-NAME = mindfulguard
VENV = $(PROJECT-NAME)-build-venv
PYTHON_VERSION = 3.10
DOCKER_WORK_DIR = docker

WIN_PATH = .\$(VENV)\Scripts
LINUX_PATH = ./$(VENV)/bin

#docker
CONTAINER_NAME = docker-postgresql-1
DATABASE_USER = mindfulguard
DATABASE_NAME = mindfulguard_production
PATH-TO-DUMP = $(DOCKER_WORK_DIR)/dumps/pgsql.sql
DOCKER_COMPOSE_YML = $(DOCKER_WORK_DIR)/docker-compose.yml

admin_login =
admin_password =
minio_hostname =
minio_root_access_key =
minio_root_secret_key =
minio_user_access_key =
minio_user_secret_key =

ifeq ($(OS),Windows_NT)
    RM = rmdir /s /q

	PATH_TO_PIP = $(WIN_PATH)\pip3.exe
	PATH_TO_PYTHON_VENV = $(WIN_PATH)\python.exe

	RUN = py -$(PYTHON_VERSION) build\__main__.py --POSTGRES_PASSWORD $(POSTGRES_PASSWORD) --POSTGRES_PASSWORD_USER $(POSTGRES_PASSWORD_USER) --POSTGRES_PASSWORD_PASSWORD $(POSTGRES_PASSWORD_PASSWORD)
	SETUP-VENV = py -$(PYTHON_VERSION) -m venv $(VENV)
	RUN-VENV = $(ACTIVATE-VENV-MSG) .\$(VENV)\Scripts\activate

	MINIO_INIT_USER =
else
    RM = rm -rf

	PATH_TO_PIP = $(LINUX_PATH)/pip3
	#it will need to be completed
	PATH_TO_PYTHON_VENV = $(LINUX_PATH)/python

	RUN = python$(PYTHON_VERSION) build/__main__.py --POSTGRES_PASSWORD $(POSTGRES_PASSWORD) --POSTGRES_PASSWORD_USER $(POSTGRES_PASSWORD_USER) --POSTGRES_PASSWORD_PASSWORD $(POSTGRES_PASSWORD_PASSWORD)
	SETUP-VENV = python$(PYTHON_VERSION) -m venv $(VENV)
	RUN-VENV = $(ACTIVATE-VENV-MSG) "source $(VENV)/bin/activate"

	MINIO_INIT_USER = chmod +x build/scripts/minio_init_user.sh && ./build/scripts/minio_init_user.sh "$(minio_hostname)" "$(minio_root_access_key)" "$(minio_root_secret_key)" "$(minio_user_access_key)" "$(minio_user_secret_key)"
endif

init:
	$(SETUP-VENV)
	$(PATH_TO_PIP) install -r build/requirements.txt
	$(PATH_TO_PYTHON_VENV) build/scripts/mindfulguard_init_admin.py $(admin_login) $(admin_password)
	$(MINIO_INIT_USER)

database-dump:
	docker exec -t $(CONTAINER_NAME) pg_dump -U $(DATABASE_USER) $(DATABASE_NAME) > $(PATH-TO-DUMP)