GO = go
PROJECT-NAME = dynamic_configurations

.PHONY: build
build:
	$(GO) build -o $(PROJECT-NAME)

.PHONY: test
test:
	$(GO) test -coverpkg=./... ./...