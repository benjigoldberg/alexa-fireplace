.PHONY: set-service install

BIN_DIR=$(GOPATH)/bin

default_target: all

all: lint test build

# Bootstrapping for base golang package deps
BOOTSTRAP=\
	github.com/golang/dep/cmd/dep \
	github.com/alecthomas/gometalinter
DEP=$(BIN_DIR)/dep
GOMETALINTER=$(BIN_DIR)/gometalinter

$(GOMETALINTER):
	go get -u github.com/alecthomas/gometalinter
	gometalinter --install &> /dev/null

$(DEP):
	go get -u github.com/golang/dep/cmd/dep

bootstrap: $(GOMETALINTER) $(DEP)

vendor: bootstrap
	dep ensure -v -vendor-only

test: vendor
	go test -race -v ./... -coverprofile=coverage.txt -covermode=atomic

coverage: test
	go tool cover -html=coverage.txt

# Linting
LINTERS=gofmt golint staticcheck vet misspell ineffassign deadcode
METALINT=gometalinter --tests --disable-all --vendor --deadline=5m -e "zz_.*\.go" ./...

lint: vendor
	$(METALINT) $(addprefix --enable=,$(LINTERS))

$(LINTERS):
	$(METALINT) --enable=$@

clean:
	rm -rf vendor

build:
	go build -ldflags="-X main.gitSHA=${GIT_SHA}" cmd/fireplace.go

ifeq ($(shell uname), Linux)
set-service:
	$(shell ln -s $(CURDIR)/fireplace.service /etc/systemd/system/fireplace.service && systemctl daemon-reload)
install: set-service
endif
install:
	$(shell GOBIN=/usr/local/bin go install cmd/fireplace.go)
