GO = go
PROJECT-NAME = dynamic_configurations

.PHONY: build
build:
	$(GO) build -o $(PROJECT-NAME)

.PHONY: test
test:
	$(GO) test -coverpkg=./... ./...

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
