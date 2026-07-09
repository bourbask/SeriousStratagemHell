.DEFAULT_GOAL := help

help:
	@echo "Usage: make <target>"
	@echo ""
	@sed -n 's/^\([a-zA-Z._-][a-zA-Z._-]*\):.*$$/  \1/p' $(MAKEFILE_LIST) | sort -u

# ── Stragetagems ──────────────────────────────────────

combos:
	@echo "Name:            $(shell python3 -c "import json,random; c=json.load(open('Data/combos.json')); t=random.choice(list(c['themes'])); s=random.choice(c['themes'][t]); print(s['name'])")"
	@echo "Inputs:          ^ v <- ->  (see main.py)"

# ── Local dev ────────────────────────────────────────

install:
	pip install -r requirements.txt

run:
	python main.py

lint:
	ruff check .

typecheck:
	pyright .

check: lint typecheck

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

.PHONY: combos install run lint typecheck check
.PHONY: worktree-ls worktree-setup cd-main cd-python cd-rust cd-go goto
