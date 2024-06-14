GO = go
PROJECT-NAME = dynamic_configurations

BUILD-DIR = build/

ifeq ($(OS),Windows_NT)
	OUTPUT-FILE = $(PROJECT-NAME).exe
else
	OUTPUT-FILE = $(PROJECT-NAME)
endif

.PHONY: build
build:
	$(GO) build -o $(BUILD-DIR)$(OUTPUT-FILE)

.PHONY: test
test:
	$(GO) test -v -tags unittests -coverpkg=./... ./...

SERVER-PORT = 9002

ifeq ($(OS),Windows_NT)
    START_SERVER := powershell -Command "Start-Process -NoNewWindow -FilePath .\$(BUILD-DIR)$(OUTPUT-FILE) -ArgumentList '-LOG-LEVEL','DEBUG','-PORT','$(SERVER-PORT)'; Start-Sleep -Seconds 1"
    STOP_SERVER := powershell -Command "Stop-Process -Name $(PROJECT-NAME) -Force"
    RUN_TESTS := powershell -Command "& { $(GO) test -v -tags servertests -coverpkg=./... ./...; if ($$LASTEXITCODE -ne 0) { $(STOP_SERVER); exit 1 } }; $(STOP_SERVER)"
else
    START_SERVER := ./$(BUILD-DIR)$(OUTPUT-FILE) -LOG-LEVEL DEBUG -PORT $(SERVER-PORT) &
    STOP_SERVER := pkill -f $(PROJECT-NAME)
    DELAY := sleep 1
    RUN_TESTS := $(GO) test -v -tags servertests -coverpkg=./... ./... ; TEST_RESULT=$$?; $(STOP_SERVER); exit $$TEST_RESULT
endif

.PHONY: test-grpc
test-grpc:
	@echo "Starting server..."
	@$(START_SERVER)
	$(DELAY)
	@echo "Running tests..."
	@$(RUN_TESTS)

PROTO-GEN-OUT-PATH = grpc/gen
PROTO-FILES-DIR = services/configuration/grpc/$(PROJECT-NAME)

ifeq ($(OS),Windows_NT)
	ROOT_DIR = $(shell powershell -Command "(Get-Location).Path | Split-Path -Parent | Split-Path -Parent")
else
	ROOT_DIR = $(shell pwd | xargs dirname | xargs dirname)
endif

PROTOC_PATH = $(ROOT_DIR)/$(PROTO-FILES-DIR)

.PHONY: gen-proto
gen-proto:
	protoc -I "$(PROTOC_PATH)" "$(PROTOC_PATH)/*.proto" --go_out=$(PROTO-GEN-OUT-PATH) --go_opt=paths=source_relative --go-grpc_out=$(PROTO-GEN-OUT-PATH) --go-grpc_opt=paths=source_relative
