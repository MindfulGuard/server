GO = go
PROJECT-NAME = dynamic_configurations

.PHONY: build
build:
	$(GO) build -o $(PROJECT-NAME)

.PHONY: test
test:
	$(GO) test -coverpkg=./... ./...

PROTO-GEN-OUT-PATH = grpc/gen
PROTO-FILES-PATH = grpc/*.proto

.PHONY: gen-proto
gen-proto:
	protoc -I grpc $(PROTO-FILES-PATH) --go_out=$(PROTO-GEN-OUT-PATH) --go_opt=paths=source_relative --go-grpc_out=$(PROTO-GEN-OUT-PATH) --go-grpc_opt=paths=source_relative