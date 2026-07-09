.DEFAULT_GOAL := help

help:
	@echo "Usage: make <target>"
	@echo ""
	@sed -n 's/^\([a-zA-Z._-][a-zA-Z._-]*\):.*$$/  \1/p' $(MAKEFILE_LIST) | sort -u

# ── Local dev ────────────────────────────────────────

install:
	cargo fetch

build:
	cargo build

run:
	cargo run

release:
	cargo build --release

test:
	cargo test

lint:
	cargo clippy -- -D warnings

fmt:
	cargo fmt --check

check: lint fmt build test

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

.PHONY: install build run release test lint fmt check
.PHONY: worktree-ls worktree-setup cd-main cd-python cd-rust cd-go goto
