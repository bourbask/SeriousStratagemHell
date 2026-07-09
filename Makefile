SHELL     := /bin/bash
PID_FILE  := .dev.pid
WORKROOT  ?= ..
PORT      ?= 5173
BROWSER   ?= xdg-open

.DEFAULT_GOAL := help

help:
	@echo "Usage: make <command>"
	@echo ""
	@sed -n 's/^\([a-zA-Z0-9._/-][a-zA-Z0-9._/-]*\):.*/\1/p' $(MAKEFILE_LIST) \
		| grep -v '^\s*\.PHONY' | sort -u | column

# ── Dev servers (background) ─────────────────────────

dev:   dev-start
dev-start:
	@rm -f $(PID_FILE)
	cd backend   && npm run dev & echo $$! >> ../$(PID_FILE)
	cd frontend  && npm run dev & echo $$! >> ../$(PID_FILE)
	sleep 2
	$(BROWSER) http://localhost:$(PORT)
	@echo "Use 'make dev-stop' to stop both servers."

dev-stop:
	@if [ -f $(PID_FILE) ]; then \
		echo "Stopping dev servers…"; \
		xargs kill < $(PID_FILE) 2>/dev/null; \
		rm -f $(PID_FILE); \
		echo "Done."; \
	else \
		echo "No dev servers running."; \
	fi

dev-backend:
	cd backend && npm run dev

dev-frontend:
	cd frontend && npm run dev

# ── Build ─────────────────────────────────────────────

build:
	$(MAKE) build-frontend

build-frontend:
	cd frontend && npm run build

# ── Checks ───────────────────────────────────────────

check:
	$(MAKE) check-ts && $(MAKE) lint && $(MAKE) build-frontend

check-ts:
	cd frontend && npx tsc --noEmit
	cd backend  && npx tsc --noEmit

lint:
	cd frontend && npm run lint

# ── Install ───────────────────────────────────────────

install:
	cd backend  && npm install
	cd frontend && npm install

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

.PHONY: help dev dev-start dev-stop dev-backend dev-frontend
.PHONY: build build-frontend check check-ts lint install goto
.PHONY: cd-main cd-python cd-rust cd-go
.PHONY: worktree-ls worktree-setup
