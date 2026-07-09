BROWSER ?= xdg-open
PORT    ?= 5173

.DEFAULT_GOAL := help

help:
	@echo "Usage: make <target>"
	@echo ""
	@sed -n 's/^\([a-zA-Z._-][a-zA-Z._-]*\):.*$$/  \1/p' $(MAKEFILE_LIST) | sort -u

# ── Local dev ────────────────────────────────────────

install: install-backend install-frontend

install-backend:
	cd backend && npm install

install-frontend:
	cd frontend && npm install

dev: dev-backend dev-frontend

dev-backend:
	cd backend && npm run dev

dev-frontend:
	cd frontend && npm run dev

build: build-frontend

build-frontend:
	cd frontend && npm run build

lint: lint-frontend

lint-frontend:
	cd frontend && npm run lint

check: check-frontend-ts check-backend-ts lint-frontend build-frontend

check-frontend-ts:
	cd frontend && npx tsc --noEmit

check-backend-ts:
	cd backend && npx tsc --noEmit

open:
	$(BROWSER) http://localhost:$(PORT)

# ── Worktree navigation ─────────────────────────────

WORKTREE_ROOT ?= ..
BRANCHES       = main python rust go

worktree-ls:
	@git worktree list
	@echo ""
	@echo "Convention:"
	@for b in $(BRANCHES); do \
		wt=$(WORKTREE_ROOT)/ssht-$$b; \
		if [ -d "$$wt" ]; then echo "  $$wt ← $$b  (exists)"; \
		else echo "  $$wt ← $$b  (not yet created)"; fi; \
	done

worktree-setup:
	@echo "Creating worktrees…"
	@for b in $(BRANCHES); do \
		wt=$(WORKTREE_ROOT)/ssht-$$b; \
		if [ ! -d "$$wt" ]; then \
			git worktree add "$$wt" "$$b" 2>&1 && echo "  ✔ $$wt ← $$b"; \
		else echo "  – $$wt already exists"; fi; \
	done
	@echo "Done. Use: make cd-<branch>"

cd-main:
	@echo cd $(WORKTREE_ROOT)/ssht-main

cd-python:
	@echo cd $(WORKTREE_ROOT)/ssht-python

cd-rust:
	@echo cd $(WORKTREE_ROOT)/ssht-rust

cd-go:
	@echo cd $(WORKTREE_ROOT)/ssht-go

goto:
	@echo "Usage: make cd-{main,python,rust,go}   → prints the cd command"
	@echo "       $$(make cd-python)              → executes the cd"

# ── Utils ────────────────────────────────────────────

.PHONY: install install-backend install-frontend dev dev-backend dev-frontend
.PHONY: build build-frontend lint lint-frontend check
.PHONY: check-frontend-ts check-backend-ts open
.PHONY: worktree-ls worktree-setup cd-main cd-python cd-rust cd-go goto
