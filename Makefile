SHELL    := /bin/bash
WORKROOT ?= ..

.DEFAULT_GOAL := help

help:
	@echo "Usage: make <command>"
	@echo ""
	@sed -n 's/^\([a-zA-Z0-9._/-][a-zA-Z0-9._/-]*\):.*/\1/p' $(MAKEFILE_LIST) \
		| grep -v '^\s*\.PHONY' | sort -u | column

# ── Run / Build ──────────────────────────────────────

run:
	go run ./cmd/seriousstratagemhell

build:
	go build ./...

# ── Tests / Checks ───────────────────────────────────

test:
	go test ./...

check:
	$(MAKE) build && $(MAKE) test && $(MAKE) lint

lint:
	golangci-lint run 2>/dev/null || echo "Install: go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest"

# ── Install ───────────────────────────────────────────

install:
	go mod tidy

# ── Navigation ───────────────────────────────────────

goto:
	@echo "Usage:  make cd-<branch>              prints the cd command"
	@echo "        eval \$$(make cd-<branch>)    executes it"
	@echo ""
	@echo "Branches: main python rust go"

cd-main:
	@echo cd $(WORKROOT)/ssht-main

cd-python:
	@echo cd $(WORKROOT)/ssht-python

cd-rust:
	@echo cd $(WORKROOT)/ssht-rust

cd-go:
	@echo cd $(WORKROOT)/ssht-go

worktree-ls:
	@git worktree list
	@echo ""
	@for b in main python rust go; do \
		wt=$(WORKROOT)/ssht-$$b; \
		if [ -d "$$wt" ]; then echo "  $$wt ← $$b  (exists)"; \
		else echo "  $$wt ← $$b  (not yet created)"; fi; \
	done

worktree-setup:
	@echo "Creating worktrees…"
	@for b in main python rust go; do \
		wt=$(WORKROOT)/ssht-$$b; \
		if [ ! -d "$$wt" ]; then \
			git worktree add "$$wt" "$$b" 2>&1 && echo "  ✔ $$wt ← $$b"; \
		else echo "  – $$wt already exists"; fi; \
	done
	@echo "Done. Use: make cd-<branch>"

.PHONY: help run build test check lint install goto
.PHONY: cd-main cd-python cd-rust cd-go
.PHONY: worktree-ls worktree-setup
